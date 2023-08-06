import os
import json
import torch

import numpy as np

from typing import *
from cftool.dist import Parallel
from cftool.misc import shallow_copy_dict
from cftool.misc import lock_manager
from cftool.misc import Saving
from cftool.misc import LoggingMixin

from .task import Task
from ..types import data_type
from ..pipeline import Pipeline
from .runs._utils import meta_config_name
from .runs._utils import data_config_file


def _task(
    task: Task,
    execute: str,
    config_folder: str,
    cuda: Optional[Union[int, str]] = None,
) -> None:
    task.run(execute, config_folder, cuda)


class ExperimentResults(NamedTuple):
    workplaces: List[str]
    workplace_keys: List[Tuple[str, str]]
    pipelines: Optional[List[Pipeline]]

    @property
    def pipeline_dict(self) -> Dict[str, Pipeline]:
        if self.pipelines is None:
            raise ValueError("pipelines are not provided")
        return dict(zip(self.workplaces, self.pipelines))


class Experiment(LoggingMixin):
    tasks_folder = "__tasks__"
    default_root_workplace = "__experiment__"

    def __init__(
        self,
        *,
        num_jobs: int = 1,
        use_cuda: bool = True,
        available_cuda_list: Optional[List[int]] = None,
    ):
        use_cuda = use_cuda and torch.cuda.is_available()
        if available_cuda_list is None and not use_cuda:
            available_cuda_list = []
        self.num_jobs = num_jobs
        self.use_cuda = use_cuda
        self.cuda_list = available_cuda_list
        self.tasks: Dict[Tuple[str, str], Task] = {}
        self.executes: Dict[Tuple[str, str], str] = {}
        self.workplaces: Dict[Tuple[str, str], str] = {}
        self.results: Optional[ExperimentResults] = None

    @staticmethod
    def data_folder(workplace: Optional[str] = None) -> str:
        workplace = workplace or Experiment.default_root_workplace
        return os.path.join(workplace, "__data__")

    @staticmethod
    def _dump_data(
        x: data_type,
        y: data_type = None,
        workplace: Optional[str] = None,
        postfix: str = "",
    ) -> None:
        data_folder = Experiment.data_folder(workplace)
        for key, value in zip([f"x{postfix}", f"y{postfix}"], [x, y]):
            if value is None:
                continue
            np.save(os.path.join(data_folder, f"{key}.npy"), value)

    @staticmethod
    def dump_data_bundle(
        x: data_type,
        y: data_type = None,
        x_cv: data_type = None,
        y_cv: data_type = None,
        *,
        workplace: Optional[str] = None,
    ) -> str:
        data_folder = Experiment.data_folder(workplace)
        os.makedirs(data_folder, exist_ok=True)
        if not isinstance(x, np.ndarray):
            data_config = {"x": x, "y": y, "x_cv": x_cv, "y_cv": y_cv}
            for k, v in data_config.items():
                if v is not None:
                    assert isinstance(v, str)
                    data_config[k] = os.path.abspath(v)
            with open(os.path.join(data_folder, data_config_file), "w") as f:
                json.dump(data_config, f)
        else:
            Experiment._dump_data(x, y, workplace)
            Experiment._dump_data(x_cv, y_cv, workplace, "_cv")
        return data_folder

    @staticmethod
    def fetch_data(
        workplace: Optional[str] = None,
        postfix: str = "",
    ) -> Tuple[data_type, data_type]:
        data = []
        data_folder = Experiment.data_folder(workplace)
        for key in [f"x{postfix}", f"y{postfix}"]:
            file = os.path.join(data_folder, f"{key}.npy")
            data.append(None if not os.path.isfile(file) else np.load(file))
        return data[0], data[1]

    @staticmethod
    def workplace(workplace_key: Tuple[str, str], root_workplace: str) -> str:
        workplace = os.path.join(root_workplace, *workplace_key)
        return os.path.abspath(workplace)

    @property
    def num_tasks(self) -> int:
        return len(self.tasks)

    def add_task(
        self,
        x: data_type = None,
        y: data_type = None,
        x_cv: data_type = None,
        y_cv: data_type = None,
        *,
        model: str = "fcnn",
        execute: str = "basic",
        root_workplace: Optional[str] = None,
        workplace_key: Optional[Tuple[str, str]] = None,
        config: Optional[Dict[str, Any]] = None,
        data_folder: Optional[str] = None,
        **task_meta_kwargs: Any,
    ) -> str:
        if workplace_key is None:
            counter = 0
            while True:
                workplace_key = model, str(counter)
                if workplace_key not in self.tasks:
                    break
                counter += 1
        if workplace_key in self.tasks:
            raise ValueError(f"task already exists with '{workplace_key}'")
        root_workplace = root_workplace or self.default_root_workplace
        workplace = self.workplace(workplace_key, root_workplace)
        copied_config = shallow_copy_dict(config or {})
        copied_config["model"] = model
        if data_folder is None and x is not None:
            data_folder = self.dump_data_bundle(x, y, x_cv, y_cv, workplace=workplace)
        if data_folder is not None:
            copied_config["data_folder"] = os.path.abspath(data_folder)
        copied_config.setdefault("use_tqdm", False)
        copied_config.setdefault("verbose_level", 0)
        copied_config.setdefault("trigger_logging", True)
        new_task = Task(workplace=workplace, config=copied_config, **task_meta_kwargs)
        self.tasks[workplace_key] = new_task
        self.executes[workplace_key] = execute
        self.workplaces[workplace_key] = workplace
        return workplace

    def run_tasks(
        self,
        *,
        use_tqdm: bool = True,
        task_loader: Optional[Callable[[str], Pipeline]] = None,
    ) -> ExperimentResults:
        parallel = Parallel(self.num_jobs, use_cuda=True, use_tqdm=use_tqdm)
        sorted_workplace_keys = sorted(self.tasks)
        sorted_tasks = [self.tasks[key] for key in sorted_workplace_keys]
        sorted_executes = [self.executes[key] for key in sorted_workplace_keys]
        sorted_workplaces = [self.workplaces[key] for key in sorted_workplace_keys]
        parallel(_task, sorted_tasks, sorted_executes, sorted_workplaces)
        if task_loader is None:
            pipelines = None
        else:
            pipelines = list(map(task_loader, sorted_workplaces))
        self.results = ExperimentResults(
            sorted_workplaces,
            sorted_workplace_keys,
            pipelines,
        )
        return self.results

    def save(self, export_folder: str, *, compress: bool = True) -> "Experiment":
        abs_folder = os.path.abspath(export_folder)
        base_folder = os.path.dirname(abs_folder)
        with lock_manager(base_folder, [export_folder]):
            Saving.prepare_folder(self, export_folder)
            # tasks
            tasks_folder = os.path.join(abs_folder, self.tasks_folder)
            for workplace_key, task in self.tasks.items():
                task.save(os.path.join(tasks_folder, *workplace_key))
            # meta
            if self.results is None:
                raise ValueError("results are not generated yet")
            meta_config = {
                "executes": self.executes,
                "num_jobs": self.num_jobs,
                "use_cuda": self.use_cuda,
                "cuda_list": self.cuda_list,
                "results": ExperimentResults(
                    self.results.workplaces,
                    self.results.workplace_keys,
                    None,
                ),
            }
            Saving.save_dict(meta_config, meta_config_name, abs_folder)
            if compress:
                Saving.compress(abs_folder, remove_original=True)
        return self

    @classmethod
    def load(cls, saving_folder: str, *, compress: bool = True) -> "Experiment":
        abs_folder = os.path.abspath(saving_folder)
        base_folder = os.path.dirname(abs_folder)
        with lock_manager(base_folder, [saving_folder]):
            with Saving.compress_loader(abs_folder, compress, remove_extracted=False):
                meta_config = Saving.load_dict(meta_config_name, abs_folder)
                experiment = cls(
                    num_jobs=meta_config["num_jobs"],
                    use_cuda=meta_config["use_cuda"],
                    available_cuda_list=meta_config["cuda_list"],
                )
                experiment.executes = meta_config["executes"]
                experiment.results = ExperimentResults(*meta_config["results"])
                # tasks
                experiment.tasks = {}
                tasks_folder = os.path.join(abs_folder, cls.tasks_folder)
                for workplace_key in experiment.workplaces:
                    task_folder = os.path.join(tasks_folder, *workplace_key)
                    experiment.tasks[workplace_key] = Task.load(task_folder)
        return experiment


__all__ = ["Experiment"]

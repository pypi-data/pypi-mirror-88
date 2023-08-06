import os

import numpy as np

from typing import *
from tqdm.autonotebook import tqdm
from cftool.misc import update_dict
from cftool.misc import shallow_copy_dict
from cftool.misc import lock_manager
from cftool.misc import Saving
from cftool.misc import LoggingMixin
from cftool.ml.utils import patterns_type
from cftool.ml.utils import Comparer
from cftool.ml.utils import Estimator
from cftool.ml.utils import ModelPattern
from cftool.ml.utils import EnsemblePattern
from cfdata.tabular import task_type_type
from cfdata.tabular import parse_task_type
from cfdata.tabular import TaskTypes

from ..dist import Task
from ..dist import Experiment
from ..dist import ExperimentResults
from ..types import data_type
from ..types import general_config_type
from ..configs import _parse_config
from ..trainer import Trainer
from ..trainer import IntermediateResults
from ..pipeline import Pipeline
from ..protocol import DataProtocol
from ..misc._api import _to_saving_path
from ..misc._api import _make_saving_path
from ..misc._api import _fetch_saving_paths
from ..misc.toolkit import to_2d


def make(
    model: str = "fcnn",
    config: general_config_type = None,
    increment_config: general_config_type = None,
    **kwargs: Any,
) -> Pipeline:
    kwargs["model"] = model
    config, increment_config = map(_parse_config, [config, increment_config])
    return Pipeline.make(update_dict(increment_config, update_dict(config, kwargs)))


def make_from(
    identifier: str = "cflearn",
    saving_folder: Optional[str] = None,
    kwargs_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    cuda: Optional[Union[int, str]] = None,
    *,
    model_mapping: Optional[Dict[str, str]] = None,
) -> Dict[str, List[Pipeline]]:
    saving_folder = os.path.abspath(saving_folder or "./")

    def _core() -> Pipeline:
        compress = os.path.isfile(f"{path}.zip")
        with lock_manager(saving_folder, [path]):
            with Saving.compress_loader(path, compress):
                kwargs = Saving.load_dict("config", path)
        if model_mapping is not None:
            kwargs["model"] = model_mapping[model]
        if cuda is not None:
            kwargs["cuda"] = cuda
        kwargs.pop("logging_folder", None)
        if kwargs.get("mlflow_config") is not None:
            kwargs["mlflow_config"] = {}
        if kwargs_callback is not None:
            kwargs_callback(kwargs)
        return make(**kwargs)

    ms: Dict[str, List[Pipeline]] = {}
    paths_dict = _fetch_saving_paths(identifier, saving_folder)
    for model, paths in paths_dict.items():
        for path in paths:
            ms.setdefault(model, []).append(_core())
    return ms


def finetune(
    x: data_type,
    y: data_type = None,
    x_cv: data_type = None,
    y_cv: data_type = None,
    *,
    model: Optional[str] = None,
    strict: bool = True,
    identifier: str = "cflearn",
    pretrain_folder: Optional[str] = None,
    kwargs_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    state_dict_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    sample_weights: Optional[np.ndarray] = None,
    cuda: Optional[Union[int, str]] = None,
) -> Pipeline:
    paths_dict = _fetch_saving_paths(identifier, pretrain_folder)
    all_paths: List[str] = sum(paths_dict.values(), [])
    if len(all_paths) > 1:
        raise ValueError("more than 1 model is detected")
    if model is None:
        model_mapping = None
    else:
        pretrain_model = list(paths_dict.keys())[0]
        model_mapping = {pretrain_model: model}
    ms = make_from(
        identifier,
        pretrain_folder,
        kwargs_callback,
        cuda,
        model_mapping=model_mapping,
    )
    m = list(ms.values())[0][0]
    m.fit(
        x,
        y,
        x_cv,
        y_cv,
        pretrain_strict=strict,
        pretrain_folder=pretrain_folder,
        pretrain_identifier=identifier,
        state_dict_callback=state_dict_callback,
        sample_weights=sample_weights,
    )
    return m


pipelines_type = Union[
    Pipeline,
    List[Pipeline],
    Dict[str, Pipeline],
    Dict[str, List[Pipeline]],
]


def _to_pipelines(pipelines: pipelines_type) -> Dict[str, List[Pipeline]]:
    if isinstance(pipelines, dict):
        pipeline_dict = {}
        for key, value in pipelines.items():
            if isinstance(value, list):
                pipeline_dict[key] = value
            else:
                pipeline_dict[key] = [value]
    else:
        if not isinstance(pipelines, list):
            pipelines = [pipelines]
        pipeline_dict = {}
        for pipeline in pipelines:
            assert pipeline.model is not None
            key = pipeline.model.__identifier__
            pipeline_dict.setdefault(key, []).append(pipeline)
    return pipeline_dict


def evaluate(
    x: data_type,
    y: data_type = None,
    *,
    contains_labels: bool = True,
    pipelines: Optional[pipelines_type] = None,
    predict_config: Optional[Dict[str, Any]] = None,
    metrics: Optional[Union[str, List[str]]] = None,
    metric_configs: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
    other_patterns: Optional[Dict[str, patterns_type]] = None,
    comparer_verbose_level: Optional[int] = 1,
) -> Comparer:
    if not contains_labels:
        msg = "`cflearn.evaluate` must be called with `contains_labels = True`"
        raise ValueError(msg)

    patterns = {}
    if pipelines is None:
        if y is None:
            raise ValueError("either `pipelines` or `y` should be provided")
        if metrics is None:
            raise ValueError("either `pipelines` or `metrics` should be provided")
        if metric_configs is None:
            metric_configs = [{} for _ in range(len(metrics))]
        if other_patterns is None:
            raise ValueError(
                "either `pipelines` or `other_patterns` should be provided"
            )
    else:
        pipelines = _to_pipelines(pipelines)
        if predict_config is None:
            predict_config = {}
        predict_config.setdefault("contains_labels", contains_labels)
        for name, pipeline_list in pipelines.items():
            first_pipeline = pipeline_list[0]
            data = first_pipeline.data
            if y is not None:
                y = to_2d(y)
            else:
                if not isinstance(x, str):
                    raise ValueError("`x` should be str when `y` is not provided")
                x, y = data.read_file(x, contains_labels=contains_labels)
                y = data.transform(x, y).y
            if metrics is None:
                metrics = [
                    k
                    for k, v in first_pipeline.trainer.metrics.items()
                    if v is not None
                ]
            if metric_configs is None:
                metric_configs = [
                    v.config
                    for k, v in first_pipeline.trainer.metrics.items()
                    if v is not None
                ]
            patterns[name] = [
                pipeline.to_pattern(**predict_config) for pipeline in pipeline_list
            ]
    if other_patterns is not None:
        for other_name in other_patterns.keys():
            if other_name in patterns:
                print(
                    f"{LoggingMixin.warning_prefix}'{other_name}' is found in "
                    "`other_patterns`, it will be overwritten"
                )
        update_dict(other_patterns, patterns)

    if isinstance(metrics, list):
        metrics_list = metrics
    else:
        assert isinstance(metrics, str)
        metrics_list = [metrics]
    if isinstance(metric_configs, list):
        metric_configs_list = metric_configs
    else:
        assert isinstance(metric_configs, dict)
        metric_configs_list = [metric_configs]

    estimators = [
        Estimator(metric, metric_config=metric_config)
        for metric, metric_config in zip(metrics_list, metric_configs_list)
    ]
    comparer = Comparer(patterns, estimators)
    comparer.compare(x, y, verbose_level=comparer_verbose_level)
    return comparer


def save(
    pipelines: pipelines_type,
    identifier: str = "cflearn",
    saving_folder: Optional[str] = None,
    *,
    compress: bool = True,
) -> Dict[str, List[Pipeline]]:
    pipeline_dict = _to_pipelines(pipelines)
    saving_path = _to_saving_path(identifier, saving_folder)
    for name, pipeline_list in pipeline_dict.items():
        for i, pipeline in enumerate(pipeline_list):
            pipeline.save(
                _make_saving_path(i, name, saving_path, True),
                compress=compress,
            )
    return pipeline_dict


def load(
    identifier: str = "cflearn",
    saving_folder: Optional[str] = None,
    *,
    compress: bool = True,
) -> Dict[str, List[Pipeline]]:
    paths = _fetch_saving_paths(identifier, saving_folder)
    pipelines = {
        k: [Pipeline.load(v, compress=compress) for v in v_list]
        for k, v_list in paths.items()
    }
    if not pipelines:
        raise ValueError(
            f"'{identifier}' models not found with `saving_folder`={saving_folder}"
        )
    return pipelines


def task_loader(saving_folder: str, compress: bool = True) -> Pipeline:
    return list(load(saving_folder=saving_folder, compress=compress).values())[0][0]


def load_experiment_results(results: ExperimentResults) -> Dict[str, List[Pipeline]]:
    pipelines_dict: Dict[str, Dict[int, Pipeline]] = {}
    for workplace, workplace_key in zip(results.workplaces, results.workplace_keys):
        pipeline = task_loader(workplace)
        model, str_i = workplace_key
        pipelines_dict.setdefault(model, {})[int(str_i)] = pipeline
    return {k: [v[i] for i in sorted(v)] for k, v in pipelines_dict.items()}


class RepeatResult(NamedTuple):
    data: Optional[DataProtocol]
    experiment: Optional[Experiment]
    pipelines: Optional[Dict[str, List[Pipeline]]]
    patterns: Optional[Dict[str, List[ModelPattern]]]

    @property
    def trainers(self) -> Optional[Dict[str, List[Trainer]]]:
        if self.pipelines is None:
            return None
        return {k: [m.trainer for m in v] for k, v in self.pipelines.items()}

    @property
    def final_results(self) -> Optional[Dict[str, List[IntermediateResults]]]:
        trainers = self.trainers
        if trainers is None:
            return None
        final_results_dict: Dict[str, List[IntermediateResults]] = {}
        for k, v in trainers.items():
            local_results = final_results_dict.setdefault(k, [])
            for trainer in v:
                final_results = trainer.final_results
                if final_results is None:
                    raise ValueError(f"training of `Trainer` ({trainer}) is corrupted")
                local_results.append(final_results)
        return final_results_dict


# If `x_cv` is not provided, then `KRandom` split will be performed
def repeat_with(
    x: data_type,
    y: data_type = None,
    x_cv: data_type = None,
    y_cv: data_type = None,
    *,
    models: Union[str, List[str]] = "fcnn",
    model_configs: Optional[Dict[str, Dict[str, Any]]] = None,
    predict_config: Optional[Dict[str, Any]] = None,
    sequential: Optional[bool] = None,
    num_jobs: int = 1,
    num_repeat: int = 5,
    temp_folder: str = "__tmp__",
    return_patterns: bool = True,
    compress: bool = True,
    use_tqdm: bool = True,
    **kwargs: Any,
) -> RepeatResult:
    if isinstance(models, str):
        models = [models]

    kwargs = shallow_copy_dict(kwargs)
    kwargs.setdefault("trigger_logging", False)
    kwargs["verbose_level"] = 0

    if sequential is None:
        sequential = num_jobs <= 1
    if model_configs is None:
        model_configs = {}

    def fetch_config(model_key: str) -> Dict[str, Any]:
        local_kwargs = shallow_copy_dict(kwargs)
        assert model_configs is not None
        local_model_config = model_configs.setdefault(model_key, {})
        return update_dict(shallow_copy_dict(local_model_config), local_kwargs)

    pipelines_dict: Optional[Dict[str, List[Pipeline]]] = None
    if sequential:
        experiment = None
        kwargs["use_tqdm"] = False
        if not return_patterns:
            print(
                f"{LoggingMixin.warning_prefix}`return_patterns` should be "
                "True when `sequential` is True, because patterns "
                "will always be generated"
            )
            return_patterns = True
        pipelines_dict = {}
        if not use_tqdm:
            iterator = models
        else:
            iterator = tqdm(models, total=len(models), position=0)
        for model in iterator:
            local_pipelines = []
            sub_iterator = range(num_repeat)
            if use_tqdm:
                sub_iterator = tqdm(
                    sub_iterator,
                    total=num_repeat,
                    position=1,
                    leave=False,
                )
            for i in sub_iterator:
                local_config = fetch_config(model)
                logging_folder = os.path.join(temp_folder, model, str(i))
                local_config.setdefault("logging_folder", logging_folder)
                m = make(model, **shallow_copy_dict(local_config))
                local_pipelines.append(m.fit(x, y, x_cv, y_cv))
            pipelines_dict[model] = local_pipelines
    else:
        if num_jobs <= 1:
            print(
                f"{LoggingMixin.warning_prefix}we suggest setting `sequential` "
                f"to True when `num_jobs` is {num_jobs}"
            )
        # data
        data_folder = Experiment.dump_data_bundle(
            x,
            y,
            x_cv,
            y_cv,
            workplace=temp_folder,
        )
        # experiment
        experiment = Experiment(num_jobs=num_jobs)
        for model in models:
            for _ in range(num_repeat):
                local_config = fetch_config(model)
                experiment.add_task(
                    model=model,
                    compress=compress,
                    root_workplace=temp_folder,
                    config=shallow_copy_dict(local_config),
                    data_folder=data_folder,
                )
        # finalize
        results = experiment.run_tasks(use_tqdm=use_tqdm)
        if return_patterns:
            pipelines_dict = load_experiment_results(results)

    patterns = None
    if return_patterns:
        assert pipelines_dict is not None
        if predict_config is None:
            predict_config = {}
        patterns = {
            model: [m.to_pattern(**predict_config) for m in pipelines]
            for model, pipelines in pipelines_dict.items()
        }

    data = None
    if patterns is not None:
        data = patterns[models[0]][0].model.data

    return RepeatResult(data, experiment, pipelines_dict, patterns)


def make_toy_model(
    model: str = "fcnn",
    config: Optional[Dict[str, Any]] = None,
    *,
    task_type: task_type_type = "reg",
    data_tuple: Optional[Tuple[data_type, data_type]] = None,
    cuda: Optional[Union[int, str]] = "cpu",
) -> Pipeline:
    if config is None:
        config = {}
    if data_tuple is not None:
        x, y = data_tuple
        assert isinstance(x, list)
    else:
        if parse_task_type(task_type) is TaskTypes.REGRESSION:
            x, y = [[0]], [[1]]
        else:
            x, y = [[0], [1]], [[1], [0]]
    data_tuple = x, y
    model_config = {}
    if model in ("fcnn", "tree_dnn"):
        model_config = {
            "pipe_configs": {
                "fcnn": {
                    "head": {
                        "hidden_units": [100],
                        "mapping_configs": {"dropout": 0.0, "batch_norm": False},
                    }
                }
            }
        }
    base_config = {
        "model": model,
        "model_config": model_config,
        "cv_split": 0.0,
        "trigger_logging": False,
        "min_epoch": 1,
        "num_epoch": 2,
        "max_epoch": 4,
        "optimizer": "sgd",
        "optimizer_config": {"lr": 0.01},
        "task_type": task_type,
        "data_config": {
            "valid_columns": list(range(len(x[0]))),
            "label_process_method": "identical",
        },
        "verbose_level": 0,
        "cuda": cuda,
    }
    updated = update_dict(config, base_config)
    return make(**updated).fit(*data_tuple)


__all__ = [
    "make",
    "make_from",
    "finetune",
    "save",
    "load",
    "evaluate",
    "task_loader",
    "load_experiment_results",
    "repeat_with",
    "make_toy_model",
    "Task",
    "Experiment",
    "ModelPattern",
    "EnsemblePattern",
    "RepeatResult",
]

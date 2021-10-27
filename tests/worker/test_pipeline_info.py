from functools import wraps
from typing import Callable

import pytest

from saturn_engine.core import Resource
from saturn_engine.worker.pipeline_info import PipelineInfo


class ResourceA(Resource):
    typename = "resource_a"


class ResourceB(Resource):
    pass


def simple_pipeline() -> None:
    ...


def pipeline_with_resources(a: ResourceA, b: "ResourceB") -> None:
    ...


class Namespace:
    def pipeline(self) -> None:
        ...


def deleted_pipeline() -> None:
    ...


def modified_pipeline() -> None:
    ...


def decorator(func: Callable) -> Callable:
    @wraps(func)
    def wrapper() -> None:
        ...

    return wrapper


@decorator
def wrapped_pipeline() -> None:
    ...


def test_pipeline_info_name() -> None:
    global deleted_pipeline, modified_pipeline

    def local_pipeline() -> None:
        ...

    assert PipelineInfo.from_pipeline(simple_pipeline) == PipelineInfo(
        module="tests.worker.test_pipeline_info", name="simple_pipeline", resources={}
    )

    assert PipelineInfo.from_pipeline(Namespace.pipeline) == PipelineInfo(
        module="tests.worker.test_pipeline_info",
        name="Namespace.pipeline",
        resources={},
    )

    assert PipelineInfo.from_pipeline(wrapped_pipeline) == PipelineInfo(
        module="tests.worker.test_pipeline_info", name="wrapped_pipeline", resources={}
    )

    with pytest.raises(ValueError):
        PipelineInfo.from_pipeline(local_pipeline)

    with pytest.raises(ValueError):
        pipeline = deleted_pipeline
        del deleted_pipeline
        PipelineInfo.from_pipeline(pipeline)

    with pytest.raises(ValueError):
        pipeline = modified_pipeline
        modified_pipeline = simple_pipeline
        PipelineInfo.from_pipeline(pipeline)


def test_pipeline_info_resources() -> None:
    assert PipelineInfo.from_pipeline(pipeline_with_resources) == PipelineInfo(
        module="tests.worker.test_pipeline_info",
        name="pipeline_with_resources",
        resources={
            "a": "resource_a",
            "b": "ResourceB",
        },
    )


def test_pipeline_info_load() -> None:
    assert (
        PipelineInfo.from_pipeline(simple_pipeline).into_pipeline() is simple_pipeline
    )
    assert (
        PipelineInfo.from_pipeline(Namespace.pipeline).into_pipeline()
        is Namespace.pipeline
    )
    assert (
        PipelineInfo.from_pipeline(wrapped_pipeline).into_pipeline() is wrapped_pipeline
    )

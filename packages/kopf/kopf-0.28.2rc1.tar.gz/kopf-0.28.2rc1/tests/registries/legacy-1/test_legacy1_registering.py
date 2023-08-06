import collections.abc

import pytest

from kopf import GlobalRegistry, SimpleRegistry


# Used in the tests. Must be global-scoped, or its qualname will be affected.
def some_fn():
    pass


def test_simple_registry_via_iter(cause_factory):

    cause = cause_factory()
    registry = SimpleRegistry()
    iterator = registry.iter_cause_handlers(cause)

    assert isinstance(iterator, collections.abc.Iterator)
    assert not isinstance(iterator, collections.abc.Collection)
    assert not isinstance(iterator, collections.abc.Container)
    assert not isinstance(iterator, (list, tuple))

    with pytest.deprecated_call(match=r"use ResourceChangingRegistry.iter_handlers\(\)"):
        handlers = list(iterator)
    assert not handlers


def test_simple_registry_via_list(cause_factory):

    cause = cause_factory()
    registry = SimpleRegistry()
    with pytest.deprecated_call(match=r"use ResourceChangingRegistry.get_handlers\(\)"):
        handlers = registry.get_cause_handlers(cause)

    assert isinstance(handlers, collections.abc.Iterable)
    assert isinstance(handlers, collections.abc.Container)
    assert isinstance(handlers, collections.abc.Collection)
    assert not handlers


def test_simple_registry_with_minimal_signature(cause_factory):

    cause = cause_factory()
    registry = SimpleRegistry()
    with pytest.deprecated_call(match=r"registry.register\(\) is deprecated"):
        registry.register(some_fn)
    with pytest.deprecated_call(match=r"use ResourceChangingRegistry.get_handlers\(\)"):
        handlers = registry.get_cause_handlers(cause)

    assert len(handlers) == 1
    assert handlers[0].fn is some_fn


def test_global_registry_via_iter(cause_factory):

    cause = cause_factory()
    registry = GlobalRegistry()
    iterator = registry.iter_cause_handlers(cause)

    assert isinstance(iterator, collections.abc.Iterator)
    assert not isinstance(iterator, collections.abc.Collection)
    assert not isinstance(iterator, collections.abc.Container)
    assert not isinstance(iterator, (list, tuple))

    with pytest.deprecated_call(match=r"use OperatorRegistry.iter_resource_changing_handlers\(\)"):
        handlers = list(iterator)
    assert not handlers


def test_global_registry_via_list(cause_factory):

    cause = cause_factory()
    registry = GlobalRegistry()
    with pytest.deprecated_call(match=r"use OperatorRegistry.get_resource_changing_handlers\(\)"):
        handlers = registry.get_cause_handlers(cause)

    assert isinstance(handlers, collections.abc.Iterable)
    assert isinstance(handlers, collections.abc.Container)
    assert isinstance(handlers, collections.abc.Collection)
    assert not handlers


def test_global_registry_with_minimal_signature(cause_factory, resource):

    cause = cause_factory()
    registry = GlobalRegistry()
    with pytest.deprecated_call(match=r"use OperatorRegistry.register_resource_changing_handler\(\)"):
        registry.register_cause_handler(resource.group, resource.version, resource.plural, some_fn)
    with pytest.deprecated_call(match=r"use OperatorRegistry.get_resource_changing_handlers\(\)"):
        handlers = registry.get_cause_handlers(cause)

    assert len(handlers) == 1
    assert handlers[0].fn is some_fn


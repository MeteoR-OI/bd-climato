import pytest
from app.tools.refManager import RefManager


@pytest.mark.unit
def test_singleton():
    ref1 = RefManager.GetInstance()
    ref1.AddRef("test", 123)
    ref2 = RefManager.GetInstance()
    assert ref2.GetRef("test") == 123


@pytest.mark.unit
def test_store_retrieve_a_reference():
    ref1 = RefManager.GetInstance()
    ref1.AddRef("test1", 123)
    assert ref1.GetRef("test1") == 123


@pytest.mark.unit
def test_store_delete_a_reference():
    ref1 = RefManager.GetInstance()
    ref1.AddRef("test2", 123)
    ref1.DelRef("test2")
    assert ref1.GetRef("test2") is None

import pytest
from main import hello, add


def test_hello():
    assert hello() == "Hello, World!"


def test_add():
    assert add(1, 2) == 3
    assert add(0, 0) == 0
    assert add(-1, 1) == 0

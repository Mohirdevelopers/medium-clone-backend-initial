import importlib.util


def test_via_importlib():
    loader = importlib.util.find_spec('decouple')
    assert loader is not None, "decouple is not installed"

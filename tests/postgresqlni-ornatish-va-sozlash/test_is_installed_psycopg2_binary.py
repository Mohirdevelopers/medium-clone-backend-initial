import importlib.util


def test_via_importlib():
    loader = importlib.util.find_spec('psycopg2')
    assert loader is not None, "psycopg2-binary is not installed"

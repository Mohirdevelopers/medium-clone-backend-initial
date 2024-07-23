

def test_via_importlib():
    try:
        import psycopg2  # noqa
        print("psycopg2-binary is installed.")
    except ImportError:
        print("psycopg2-binary is not installed.")

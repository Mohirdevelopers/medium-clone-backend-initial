import importlib.util
from django.db import connections
from django.db.utils import OperationalError
import pytest


def test_via_importlib():
    loader = importlib.util.find_spec('psycopg2')
    assert loader is not None, "psycopg2-binary is not installed"


@pytest.mark.django_db
def test_database_connectivity():
    db_conn = connections['default']
    assert db_conn.vendor == 'postgresql', "postgresql is not configured"
    try:
        c = db_conn.cursor()
        c.execute("SELECT 1")
        c.fetchone()
    except OperationalError:
        assert False, "cannot connect to postgresql"

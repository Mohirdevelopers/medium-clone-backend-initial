import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_custom_user_meta_class():
    meta = User._meta

    index_names = {index.name for index in meta.indexes}
    expected_indexes = {
        'customuser_first_name_hash_idx',
        'customuser_last_name_hash_idx',
        'customuser_middle_name_hash_idx',
        'customuser_username_idx'
    }
    assert expected_indexes.issubset(index_names)

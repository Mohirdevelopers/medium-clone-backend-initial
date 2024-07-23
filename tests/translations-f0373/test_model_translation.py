import pytest
from django.contrib.auth import get_user_model
from django.utils import translation
from django.conf import settings
from modeltranslation.translator import translator

User = get_user_model()


@pytest.mark.django_db
def test_modeltranslation_is_setup_correctly(user_factory):
    assert translator.get_options_for_model(User) is not None

    instance = user_factory.create(first_name="Test")

    for lang_code, _ in settings.LANGUAGES:
        field_name = f'first_name_{lang_code}'
        assert hasattr(instance, field_name), f"{field_name} not found in {User.__name__}"

    instance.first_name_en = "English name"
    instance.first_name_uz = "O'zbekcha ism"
    instance.first_name_ru = "Русское имя"
    instance.save()

    instance.refresh_from_db()

    with translation.override('en'):
        assert instance.first_name == "English name"
    with translation.override('uz'):
        assert instance.first_name == "O'zbekcha ism"
    with translation.override('ru'):
        assert instance.first_name == "Русское имя"

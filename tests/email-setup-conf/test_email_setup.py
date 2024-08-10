import pytest
import importlib


@pytest.mark.order(1)
def test_send_email_service_class():
    module_name = "users.services"
    class_name = "SendEmailService"

    try:
        module = importlib.import_module(module_name)
        assert hasattr(module, class_name), f"{class_name} is not found in {module_name}"
    except ImportError:
        pytest.fail(f"Module {module_name} is missing or not correctly imported")

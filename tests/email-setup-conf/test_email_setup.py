import pytest
import importlib

@pytest.mark.order(1)
def test_env_example_file():
    required_settings = [
        "EMAIL_BACKEND",
        "EMAIL_HOST",
        "EMAIL_USE_TLS",
        "EMAIL_PORT",
        "EMAIL_HOST_USER",
        "EMAIL_HOST_PASSWORD",
    ]

    try:
        with open(".env.example", "r") as file:
            content = file.read()
            for setting in required_settings:
                assert f"{setting}=" in content, f"{setting} is missing in .env.example"
    except FileNotFoundError:
        pytest.fail(".env.example file is missing")


@pytest.mark.order(2)
def test_send_email_service_class():
    module_name = "users.services"
    class_name = "SendEmailService"

    try:
        module = importlib.import_module(module_name)
        assert hasattr(module, class_name), f"{class_name} is not found in {module_name}"
    except ImportError:
        pytest.fail(f"Module {module_name} is missing or not correctly imported")

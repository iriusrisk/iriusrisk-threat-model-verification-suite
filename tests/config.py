import os
import iriusrisk_python_client_lib
import pytest
import yaml
from pathlib import Path


def setup():
    try:
        file = os.environ['CONFIG_FILE']
    except KeyError:
        file = "example.yaml"

    f = open(Path.cwd() / file, "r")
    configuration = yaml.load(f, yaml.SafeLoader)
    f.close()

    api_token = configuration["apiToken"]
    config = configuration["config"]

    product_ref = configuration["productRef"]
    api_instance = iriusrisk_python_client_lib.ProductsApi(iriusrisk_python_client_lib.ApiClient())
    api_instance.api_client.configuration.host = configuration["server"]

    # TODO: Remove this
    api_token = "83890825-6ffb-4e57-a443-93c89559a44b"
    api_instance.api_client.configuration.host = "http://172.28.16.1:8080/api/v1"

    # Testing connectivity
    try:
        api_instance.products_get(api_token)
    except:
        pytest.fail(f"No connectivity with {configuration['server']}")

    return api_token, config, product_ref, api_instance

def check(name, config):
    test_config = list((x for x in config if x["testName"] == name))
    if not test_config:
        pytest.skip("No test config")
    else:
        return test_config[0]
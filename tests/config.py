import os
import iriusrisk_python_client_lib
import pytest
import yaml
from pathlib import Path


def setup():

    # Load the configuration file. Fails the test if no config have been found
    filename = ""
    try:
        filename = os.environ['TMVS_CONFIG'] + ".yaml"
    except KeyError:
        pytest.fail("No configuration found. Please indicate configuration in CONFIG_FILE environment variable")

    # Load configuration parameters
    f = open(Path.cwd() / filename, "r")
    configuration_file = yaml.load(f, yaml.SafeLoader)
    f.close()
    test_config = configuration_file["config"]

    # If environment variables are set, we override them
    try:
        server = os.environ['IRIUS_SERVER']
    except KeyError:
        server = configuration_file.get("server")

    try:
        api_token = os.environ['IRIUS_API_TOKEN']
    except KeyError:
        api_token = configuration_file.get("apiToken")

    try:
        product_ref = os.environ['PRODUCT_REF']
    except KeyError:
        product_ref = configuration_file.get("productRef")

    if server is None:
        pytest.fail("Server not found. Please indicate configuration in IRIUS_SERVER environment variable or 'server' key in configuration file")
    if api_token is None:
        pytest.fail("API token not found. Please indicate configuration in IRIUS_API_TOKEN environment variable or 'apiToken' key in configuration file")
    if product_ref is None:
        pytest.fail("Product ref not found. Please indicate configuration in PRODUCT_REF environment variable or 'productRef' key in configuration file")

    # Create the api_instances
    api_client = iriusrisk_python_client_lib.ApiClient()
    api_client.configuration.host = server + "/api/v1"
    api_client.configuration.api_key = api_token
    api_instance = iriusrisk_python_client_lib.ProductsApi(api_client)

    return api_token, test_config, product_ref, api_instance


def check(name, config):
    test_config = list((x for x in config if x["testName"] == name))
    if not test_config:
        pytest.skip("No test config")
    else:
        return test_config[0]

# IriusRisk Threat Model Verification Suite

This project aims to help users to integrate IriusRisk in their CI/CD environments by providing a Docker image to automate the querying to the threat model.

## Requirements

Docker must be installed previously in order to pull the image. 
```
docker pull continuumsecurity/iriusrisk-tmvs
```
You can pull the image previously or let Docker handle the pulling when running the container for the first time
Latest version is 1.0.0 (01/12/2020)

## How to use

This tool has been conceived to be as easy to configure as possible so there are three ways to use it:

### Option 1: Run one of our predefined configurations

IriusRisk TMVS contains a set of predefined configurations that execute a set of our tests. 

You will need to pass the following parameters to the docker run command:
* IRIUS_SERVER: IriusRisk instance server ([http|https]://\<host>:\<port>)
* IRIUS_API_TOKEN: IriusRisk API token from an IriusRisk user.
* PRODUCT_REF: IriusRisk threat model reference
* CONFIG_FILE: one of the names of the above list.

Example:
```
docker run --rm -e IRIUS_SERVER=<server> -e IRIUS_API_TOKEN=<token> -e PRODUCT_REF=<product_ref> -e CONFIG_FILE=risk iriusrisk-tmvs
```

### Option 2: Create and run your own configuration

If our predefined configurations are not enough and you want to tune your own configurations you need to define a volume to pass the configuration file to the container. 

```
docker run --rm -v /path/to/yamls:/volume -e CONFIG_FILE=custom iriusrisk-tmvs
```

Note that "/path/to/yamls" is a folder in the Docker host system and must be changed.
It is also mandatory to pass the name of the yaml file to execute with the CONFIG_FILE environment variable.
User folder must be linked with /volume.

__Example__: suppose that you have a folder called "/home/user/yamlFiles" that contains test1.yaml, test2.yaml and test3.yaml
You can then run the following:
```
docker run --rm -v /home/user/yamlFiles:/volume -e CONFIG_FILE=test1 iriusrisk-tmvs
```

Please check [here](#yaml-configuration) to see how to configure the Yaml file.

__Information for Windows users__: you may need to replace "/path/to/yamls" with "c:/path/to/yamls" or any other disk drive letter.


### Option 3: Create your own tests

In case you want to write your own tests you should download the repository directly.

Ensure you have at least Python 3.7 installed as well as Pip before proceeding with the following steps:
```
# Download the IriusRisk Python client library
git clone https://github.com/iriusrisk/iriusrisk-python-client-lib.git
pip install iriusrisk-python-client-lib/iriusrisk-python-client-lib
# Download the IriusRisk TMVS
git clone https://github.com/iriusrisk/iriusrisk-threat-model-verification-suite.git
# Install the requirements with pip
cd iriusrisk-threat-model-verification-suite
pip install -r requirements.txt
# To execute the tests launch the following command
pytest --junitxml=result.xml
```
You may want to change some of the steps if you want to use a virtual environment like venv.

To create your tests you will find a template ready to be used called test_custom.py inside /tests.
Keep in mind that this template uses config.py functions to avoid repeating configurations, so you should focus on create test functions using the variables inside self variable.



## Yaml configuration

This is a configuration file example in which you can see how the format is:

```
server: http://host:8080
apiToken: 83890825-6ffb-4e57-a443-93c89559a44b
productRef: test
config:
  - testName: test_residual_risk_over_risk_threshold
    variables:
      RISK_THRESHOLD: 70
  - testName: test_custom_test
    variables:
      PARAMETER: value
  - testName: test_custom_test_without variables
  - testName: test_custom_test_2
    variables:
      RISK_THRESHOLD: 70
```
"server" and "apiToken" must be changed to the corresponding ones.
Tests are executed for one project. Users must indicate the project reference in the "projectRef" parameter.
"testName" parameters must be specified with the actual names of the tests.

Note that our predefined tests only have the "config" key because they assume the other parameters will come from environment variables.

## Available tests
#### Version 1.0.0
* __test_residual_risk_over_risk_threshold__: shows if the current risk of a product exceed a risk threshold
  * RISK_THRESHOLD: number from 0 to 100. Default value is 50.
* __test_required_controls_not_implemented__: shows how many required controls are not implemented
  * PERCENTAGE: maximum percentage allowed until failure. Default value is 50.
* __test_standard_controls_not_implemented__: shows how many required controls related to a standard are not implemented
  * STANDARD_REF: standard reference value
  * PERCENTAGE: maximum percentage allowed until failure. Default value is 50.
* __test_high_risk_controls_not_implemented__: shows how many controls with high risk are not implemented
  * HIGH_RISK_VALUE: minimum value for a countermeasure to be of high risk. Default value is 75.
  * PERCENTAGE: maximum percentage allowed until failure. Default value is 50.

Configurations available are:
* __risk__: tests related with risk rating analysis
  * Tests:
    * test_residual_risk_over_risk_threshold
* __controls__: tests related with implemented countermeasures
  * Tests:
    * test_required_controls_not_implemented
    * test_high_risk_controls_not_implemented


  
## Examples
#### GoCD
```
format_version: 9

pipelines:
  IriusRisk-TMVS:
    group: Development
    materials:
      mygit: 
        git: http://my.example.org/mygit.git
        branch: ci

    stages:
      - update:
          fetch_materials: false
          jobs:
            docker:
              tasks:
               - exec:
                  command: /bin/bash
                  arguments:
                   - -e
                   - -c
                   - "docker run --rm -v /path/with/yamls:/volume -e CONFIG_FILE=custom iriusrisk-tmvs"
```
#### Jenkins
```
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh "docker run --rm -v /path/with/yamls:/volume -e CONFIG_FILE=custom -e IRIUS_SERVER=<server> -e IRIUS_API_TOKEN=<token> iriusrisk-tmvs"
            }
        }
    }
}
```

<img width="200" src="https://iriusrisk.com/wp-content/uploads/2020/10/logo-iriusrisk.svg">

# IriusRisk Threat Model Verification Suite
This project aims to support users with the integratation of IriusRisk into their CI/CD environments. A Docker image is used to automate the threat model querying. Pytest is used to generate a failure test report from the process.

## Requirements
Docker must be previously installed in order to pull the image. 
```
docker pull continuumsecurity/iriusrisk-tmvs
```
You can pull the image using a specific tag that matches the version or use the :latest tag.

Latest version is 1.0.0 (01/12/2020)

## How to use
The tool is easily configured, there are three ways to use it:

### Option 1: Run one of our predefined configurations
IriusRisk TMVS contains a set of predefined configurations that execute a set of our tests. 

You will need to pass the following parameters to the docker run command:
* IRIUS_SERVER: IriusRisk instance server ([http|https]://\<host>:\<port>)
* IRIUS_API_TOKEN: IriusRisk API token from an IriusRisk user
* PRODUCT_REF: IriusRisk threat model reference
* TMVS_CONFIG: one of the names in this [list](#available-tests-and-configurations)

```
docker run --rm -e IRIUS_SERVER=<server> -e IRIUS_API_TOKEN=<token> -e PRODUCT_REF=<product_ref> -e TMVS_CONFIG=<test_configuration> continuumsecurity/iriusrisk-tmvs
```
Example:
```
docker run --rm -e IRIUS_SERVER=http://myserver:8080 -e IRIUS_API_TOKEN=13084772-ef51-40f1-9d74-eadd4953fb10 -e PRODUCT_REF=my-product-ref -e TMVS_CONFIG=risk continuumsecurity/iriusrisk-tmvs
```

Once the commands have been executed there will be a console output from pytest and a file generated called result.xml which will be stored in the /volume folder inside the container.
If you want to obtain the result file you will need to configure the appropiate volume. See the next step to see how to do it.


### Option 2: Create and run your own configuration

If our predefined configurations are not enough and you want to tune your own configurations you need to define a volume to pass the configuration file to the container. 

```
docker run --rm -v /path/to/yamls:/volume -e TMVS_CONFIG=<custom_name> continuumsecurity/iriusrisk-tmvs
```
Note that "/path/to/yamls" is a folder in your Docker host system and must be changed with the absolute path of your configuration folder.
It is also mandatory to pass the name of the yaml file to execute with the TMVS_CONFIG environment variable.
User folder must be linked with /volume using the option "-v /path/to/yamls:/volume".

__Example__: suppose that you have a folder called "/home/user/yamlFiles" that contains test1.yaml, test2.yaml and test3.yaml

You can then run the following:
```
docker run --rm -v /home/user/yamlFiles:/volume -e TMVS_CONFIG=test1 continuumsecurity/iriusrisk-tmvs
```

Please check [here](#yaml-configuration) to see how to configure the Yaml file.

__Information for Windows users__: you may need to replace "/path/to/yamls" with "c:/path/to/yamls" or any other disk drive letter.


### Option 3: Create your own tests

In the case that you want to write your own tests you should directly download the repository.

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
pytest --junitxml=result.xml --tb=line
```
You may have to change some of the steps if you want to use a virtual environment like venv.

To create your tests you will find a pre-prepared template ready for use called test_custom.py inside folder /tests.
Keep in mind that this template uses config.py functions to avoid repeating configurations, so you should focus on creating test functions using the variables inside the self variable.



## Yaml configuration

This is a configuration file example showing the format:

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
Tests are executed for a specific project. Users must indicate the project reference in the "productRef" parameter.
"testName" parameters must be specified with the actual names of the tests.

Note that our predefined tests only have the "config" key because they assume the other parameters will come from the environment variables.

## Available configurations and Tests
#### Available configurations

* __risk__: tests related with risk rating analysis
  * test_residual_risk_over_risk_threshold
* __controls__: tests related with implemented countermeasures
  * test_required_controls_not_implemented
  * test_high_risk_controls_not_implemented

#### Available tests
* __test_residual_risk_over_risk_threshold__: shows if the current risk of a product exceeds a risk threshold
  * RISK_THRESHOLD: number from 0 to 100. 
    * Default value is 75.
* __test_required_controls_not_implemented__: shows how many required controls are not implemented
  * PERCENTAGE: maximum percentage allowed until failure. 
    * Default value is 50.
* __test_standard_controls_not_implemented__: shows how many required controls related to a standard are not implemented
  * STANDARD_REF: standard reference value
  * PERCENTAGE: maximum percentage allowed until failure. 
    * Default value is 50.
* __test_high_risk_controls_not_implemented__: shows how many controls with high risk are not implemented
  * HIGH_RISK_VALUE: minimum value for a countermeasure to be of high risk. 
    * Default value is 75.
  * PERCENTAGE: maximum percentage allowed until failure. 
    * Default value is 50.



#### I missed some tests here that could be very helpful, do I have to do it myself?

Please [reach us](https://iriusrisk.com/contact/) and share your thoughts! We want this tool to be helpful for everyone and your problem today could be a problem for someone tomorrow.
  
## Examples
#### Jenkins
```
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh "docker run --rm -v /path/with/yamls:/volume -e TMVS_CONFIG=custom -e IRIUS_SERVER=<server> -e IRIUS_API_TOKEN=<token> continuumsecurity/iriusrisk-tmvs"
            }
        }
    }
}
```

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
                   - "docker run --rm -v /path/with/yamls:/volume -e TMVS_CONFIG=custom continuumsecurity/iriusrisk-tmvs"
```

#### Github Actions
```
name: IriusRisk TMVS Workflow

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: run suite
        run: docker run --rm -e IRIUS_SERVER=${{ secrets.IRIUS_SERVER }} -e IRIUS_API_TOKEN=${{ secrets.IRIUS_API_TOKEN }} -e PRODUCT_REF=${{ secrets.PRODUCT_REF }} -e TMVS_CONFIG=${{ secrets.TMVS_CONFIG }} continuumsecurity/iriusrisk-tmvs:latest
    
```

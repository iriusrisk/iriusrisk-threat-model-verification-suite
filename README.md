# IriusRisk Threat Model Verification Suite

This project aims to help users to integrate IriusRisk in their CI/CD environments by providing a Docker image to automate the querying to the threat model.

## Requirements

Docker must be installed previously in order to create the image.
```
docker pull iriusrisk-tmvs:1.0.0
```

## How to use

Once the image is pulled users can run the following command in their automation servers (Jenkins, GoCD, etc.).

On Windows:
```
docker run --rm -v c:/path/to/folder/with/yamls:/volume -e CONFIG_FILE=example.yaml iriusrisk-tmvs:1.0.0
```
On Linux:
```
docker run --rm -v /path/to/folder/with/yamls:/volume -e CONFIG_FILE=example.yaml iriusrisk-tmvs:1.0.0
```

Note that "/path/to/folder/with/yamls" is a folder in the Docker host system and must be changed.
It is also mandatory to pass the name of the yaml file to execute with the CONFIG_FILE environment variable.
User folder must be linked with /volume.

__Example__: suppose that you have a folder called "/home/user/yamlFiles" that contains test1.yaml, test2.yaml and test3.yaml
You can then run the following:
```
docker run --rm -v /home/user/yamlFiles:/volume -e CONFIG_FILE=test1.yaml iriusrisk-tmvs:1.0.0
```



## Yaml configuration

There is an example called example.yaml in which you can see how the format is:

```
server: http://host:8080
apiToken: 83890825-6ffb-4e57-a443-93c89559a44b
productRef: test
config:
  - testName: test_residual_risk_over_risk_threshold
    variables:
      RISK_THRESHOLD: 70
  - testName: test_template
    variables:
      MULTIPLE: DATA TYPES
      a: 123                     # an integer
      b: "123"                   # a string, disambiguated by quotes
      c: 123.0                   # a float
      d: !!float 123             # also a float via explicit data type prefixed by (!!)
      e: !!str 123               # a string, disambiguated by explicit type
      f: !!str Yes               # a string via explicit type
      g: Yes                     # a boolean True (yaml1.1), string "Yes" (yaml1.2)
      h: Yes we have No bananas  # a string, "Yes" and "No" disambiguated by context.
      VARIABLES_CAN_BE_EMPTY:
      ALSO_IT_IS_NOT_MANDATORY_TO_HAVE_VARIABLES_IN_A_TEST:
  
```

"server" and "apiToken" must be changed to the corresponding ones.
Tests are executed for one project. Users must indicate the project reference in the "projectRef" parameter.

```
docker run --rm -e CONFIG_FILE=example.yaml iriusrisk-tmvs:1.0.0
```
Remember! This is just an example that always will work. You have to configure a volume with option ```-v /path/to/folder/with/yamls:/volume``` as you saw before.

## Available tests
#### Version 1.0.0
* __test_template__: example test, doesn't do anything
* __test_residual_risk_over_risk_threshold__: outputs a list of products that exceed a risk threshold
  * RISK_THRESHOLD: number from 0 to 100. Default value is 50.
  
## Examples
#### GoCD
```
format_version: 9

pipelines:
  IriusRisk-Testing-Suite:
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
                   - "docker run --rm -v /path/to/folder/with/yamls:/volume -e CONFIG_FILE=example.yaml iriusrisk-tmvs:1.0.0"
```


## Customize tests

In case you want to integrate custom tests users can use pytest to execute the suite.
Make sure you have the required dependencies installed (python, pip, iriusrisk_python_client_lib)

Inside /tests there is an example of a custom test file. Please use this template to create your own content.

```
python -m pytest -v tests --junitxml=result.xml
```



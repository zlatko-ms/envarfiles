# varfiletoenv

This action reads the definitions of variables from a set of files and injects them in the github environnement variables set.

It provides a conveniant way of centralizing the project variables defintions in the source control and allows to use them saeamlessly from your source code or from the github workflows.

In short the benefits are the following : 

* avoid declaring the same variables in different workflows 
* avoid duplication of variable declaration between your source code files and the GitHub project variable settings.

For more information on github action variables please check [Variables](https://docs.github.com/en/actions/learn-github-actions/variables) 

## Inputs

| Name      | Required | Description                                                                                     | Default Value             |
| --------- | -------- | ------------------------------------------------------------------------------------------------| ------------------------- |
| paths     | Yes      | The paths of files that contain the definitions of the variable                                 | ./project.vars.properties |
| override  | No       | Indicates if already existing workflow variables should be updated with defintions from file(s) | true |
| logs      | No       | Indicates whenever to provide internal actions logs, handy in case of troubleshooting           | false |


## Example usages 

### Basic usage 

Let's consider your variables are defined in the *./src/main/resources/versions.txt* file : 

```bash
cat ./src/main/resources/versions.txt
SW_RELEASE=1.0.0
SW_TAG=latest
```

In order to create the github env variables from this file, simply use the action in it's simplest form : 

```yaml
uses: zlatko-ms/varfiletoenv@v1
with:
  paths: ./src/main/resources/versions.txt
```

### Multiple files

Let's consider your variables are dispatched between *./src/main/resources/versions.txt* and *./src/main/resources/tags.txt* : 

```bash
cat ./src/main/resources/versions.txt
SW_RELEASE=1.0.0
cat ./src/main/resources/tags.txt
SW_TAG=latest
```

In order to create the github env variables from the above listed files, just provide multiple paths : 

```yaml
uses: zlatko-ms/varfiletoenv@v1
with:
  paths: |
    ./src/main/resources/versions.txt
    ./src/main/resources/tags.txt
```

### Override control

The default behaviour of the action is to override the definitions of the github env variables if they are present in the definition file(s).


If you'd like to disable the override behaviour and make sure your local workflow variables are preserved, the use the override input parameter : 

```yaml
    - name: Import project variables with overriding
      uses: zlatko-ms/varfiletoenv@v1
      with:
        override: false
        paths: ./src/main/resources/tags.txt
```

## Global example

If you'd like to see all the possibilities of this action, pleaase take a look at the [test github action workflow](./.github/workflows/test.yml) provided with the project.

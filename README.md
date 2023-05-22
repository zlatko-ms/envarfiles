# varfiletoenv

This action reads the definitions of variables from a set of files and injects them in the github environnement variables set.

It provides a conveniant way of centralizing the project variables defintions in the source control and allows to use them saeamlessly from your source code or from the github workflows.

In short the benefits are the following : 

* avoid declaring the same variables in different workflows 
* avoid duplication of variable declaration between your source code files and the GitHub project variable settings.

For more information on github action variables please check [Variables](https://docs.github.com/en/actions/learn-github-actions/variables) 

## Inputs

### paths

**Required** the paths to the files that contains variable defintions. Defaults to *"project.vars.properties"*.

### override

**Optional** set to False if you do not want to override already existing variables defined in the workflow. Defaults to *"true"*.

## Example usage 

### Basic usage 

Let's consider your variables are defined in the *./src/main/resources/versions.txt* file : 

```bash
cat ./src/main/resources/versions.txt
SW_RELEASE=1.0.0
SW_TAG=latest
```

In order to create the variables in the github project env placeholder, all you have to do is the following : 

```yaml
uses: actions/varfiletoenv@main
with:
  paths: ./src/main/resources/versions.txt
```

### Multiple files

Let's consider your variables are dispatched between *./src/main/resources/versions.txt* and *./src/main/resources/tags.txt* file : 

```bash
cat ./src/main/resources/versions.txt
SW_RELEASE=1.0.0
cat ./src/main/resources/tags.txt
SW_TAG=latest
```
In order to create the variables in the github project env placeholder, all you have to do is the following : 

```yaml
uses: actions/varfiletoenv@main
with:
  paths: |
    ./src/main/resources/versions.txt
    ./src/main/resources/tags.txt
```

### Overrde control

Per default the action will override all the values with the ones defined in the file set.

If you'd like to make sure no override happens to your locally defined variabales, just specify the override flag to false : 

```yaml
    - name: Import project variables with overriding
      uses: zlatko-ms/varfiletoenv@2-add-support-for-override-flag
      with:
        override: false
        paths: ./src/main/resources/tags.txt
```

### Global example

If you'd like to see all the possibilities of this file, the most conveninent way is to check the source of the 
[test github action workflow](./.github/workflows/test.yml) provided with the project.

# OLD 

A global example would look like this : 

```yaml

name: Greeting on variable day

on:
  workflow_dispatch

jobs:
  example_job:
    
    runs-on: ubuntu-latest
    
    env:
      WorkflowLocalVar: Value1

    steps:
      - name: "Import project variables from source file "
        uses: actions/varfiletoenv@main
        with:
            paths: ./src/main/resources/versions.txt

      - name: "Display available variables "
        run: |
            echo "workflow defined variable in env section :  " ${{ env.WorkflowLocalVar }}
            echo "defined from source, software release    :  " ${{ env.SW_RELEASE }
            echo "defined from source, software tag        :  " ${{ env.SW_TAG }

```
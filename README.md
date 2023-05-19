# Ghprojectvars

This action reads a file for variable definitions and injects them in the github envirommenent variable set for each required workflow.

Using this action you'll get the following benefits : 

* avoid declaring the same variables in different workflows , as you can inject all the defs in each workflow 
* avoid duplication of variable definitions between your source code and the GitHub project variable settings.

For more information on github action variables please check [Variables](https://docs.github.com/en/actions/learn-github-actions/variables) 

## Inputs

### varfilepath

**Required** the path to the file that contains variable defintions. Default to "PROJECTVARS.cfg"

## Outputs

### definitions

List of VariableName=VariableValue values injected in the github environnement.

## Example usage 

Let's consider your variables are defined in the *./src/main/resources/projectvars.txt* file : 

```bash
cat ./src/main/resources/projectvars.txt
SW_RELEASE=1.0.0
SW_TAG=latest
```

In order to create the variables in the github project env placeholder, all you have to do is the following : 

```yaml
uses: actions/ghprojectvars@main
with:
  varfilepath: './src/main/resources/projectvars.txt'
```

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
        uses: actions/ghprojectvars@main
        with:
            varfilepath: ./src/main/resources/projectvars.txt

      - name: "Display available variables "
        run: |
            echo "workflow defined variable in env section :  " ${{ env.WorkflowLocalVar }}
            echo "defined from source, software release    :  " ${{ env.SW_RELEASE }
            echo "defined from source, software tag        :  " ${{ env.SW_TAG }

```

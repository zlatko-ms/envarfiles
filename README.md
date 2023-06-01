[![Action Build and Test](https://github.com/zlatko-ms/envarfiles/actions/workflows/buildtest.yml/badge.svg)](https://github.com/zlatko-ms/envarfiles/actions/workflows/buildtest.yml)

# Env Var Files

The action imports variables defeined in files (plain text, json, yaml) into the GitHub workflow env variable set. 

It provides the following benefits : 

* centralize variable definitions in the source control
* share variables between different workflows/jobs 
* share variables between your app code and the github workflows

For more information on github action variables please check [Variables](https://docs.github.com/en/actions/learn-github-actions/variables) 

# Inputs

| Name      | Required | Description                                                                                     | Default Value             |
| --------- | -------- | ------------------------------------------------------------------------------------------------| ------------------------- |
| paths     | Yes      | The paths of files that contain the definitions of the variable                                 | ./project.vars.properties |
| override  | No       | When set to true, the processing will override the already defined vars in the job with the values read from file  | false |
| select    | No       | When non empty, the parameter indicates the list of the variables to import from the fileset. In that case only the listed variables will be imported, other discovered varaibles will be ignored. When empty all discovered variables will be imported | '' |
| separator | No       | Override the default separator for nested properties that can be part of structured files (json, yaml) | '_' |

# Supported Formats

This version supports variables defied from plain text and json files.

The format will be determined by the file extensions : 
* JSON : .json
* YAML : .yaml, .yml
* Plain Text : all but .json, .yml and .yaml

## Plain Text Files

Plain text files (.properties, .conf, .whaever ) expect to provide key=value definitions such as : 

```
VariableName=Value
```

Note that the parser will ignore all lignes starting with **standard scripting** ("#") and ***Java/JS** ("//", "/**" , " * " , "*/") **comments**. It will also remove all trailig spaces from the line.

For instance the following variable definitions file will inject a variable named VariableName with the value 'New Value' :

```
# old definition
# VariableName=OldValue
# this is the current variable definition
 VariableName = New Value
```

## JSON Files

The action supports JSON files and handles nested properties declaration. 

Nested properties will be separated by an underscore ("_") before injection.

For instance, the following JSON content : 

```json
{ 
 "build" : { 
  "version" : {
   "major" : "1",
   "minor" : "0",
   "patch" : "42"
    }
  }
}
```
will inject the following variables : 

```
build_version_major=1
build_version_minor=0
build_version_patch=42
```

Please note that the parser will only process *fully compliant JSON object declarations* ( i.e : { "K" : "V" } ).

The parsing of lists of objects such as *{ [ {"build" : "always" } , { "tag" : "latest" } ] }* is not supported.

## YAML Files

The action supports JSON files and handles nested properties declaration. 

Nested properties will be separated by an underscore ("_") before injection.


For instance, the following YAML content : 

```yaml
build:
  version:
    major: "1"
    minor: "2"
```
will inject the following variables : 

```
build_version_major=1
build_version_minor=2
```

# Known issues

The parsing of the structured formats (JSON and YAML) does not support correctly variables with array values.

Consider the following example files : 

```json
{ "envs" : [ "dev" , "test", "prod "]}
```

```yaml
envs:
  - dev
  - test
  - prod
```

In the current state, the above mentionned payloads parsing will create the following vars : 

```
envs_1:dev
envs_2:test
envs_3:prod
```

Whenever possible we advise to consider an alternative declaration for listed values and to post process them. 

For instance the above example should be written as :  

```json
{ "envs" : "dev,test,prod" }
```

# Example usages 

In order to import all vars from a single file, simply use : 

```yaml
  - name: Import vars example
    uses: zlatko-ms/varfiletoenv@v2
    with:
      paths: ./path/to/my/file.properties
```

All usages are illustrated by the integration tests implemented in the main action workflow directory.

Here is a selection of the common usages : 


| Use Case                 | Description                                                                   | Link     |
| ------------------------ | ----------------------------------------------------------------------------- |----------|
| Load from multiple files | Load variables from multiple files and formats                                | [view](.github/workflows/it-multiformat.yml?plain=1#L19-L25)
| Override existing values | Override the values of already defined variables                              | [view](.github/workflows/it-override.yml?plain=1#L23-L30)
| Select variables         | Load or override only variables that are specified in the selector            | [view](.github/workflows/it-select.yml?plain=1#L18-L29)
| Change nested separator  | Loaded nested variables using a specific separator instead of the default "_"  | [view](.github/workflows/it-separator.yml?plain=1#L19-L25)

When copying/pasting from the examples, remember to replace the @main tag by the release tag [ currently @v3 ].

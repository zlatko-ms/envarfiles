# varfiletoenv

The action imports variables defeined in files (plain text, json ) into the GitHub workflow env variable set. 

It provides the following benefits : 

* centralize variable definitions in the source control
* share variables between different workflows/jobs 
* share variables between your app code and the github workflows

For more information on github action variables please check [Variables](https://docs.github.com/en/actions/learn-github-actions/variables) 

# Inputs

| Name      | Required | Description                                                                                     | Default Value             |
| --------- | -------- | ------------------------------------------------------------------------------------------------| ------------------------- |
| paths     | Yes      | The paths of files that contain the definitions of the variable                                 | ./project.vars.properties |
| override  | No       | Indicates if already existing workflow variables should be updated with defintions from file(s) | true |
| logs      | No       | Indicates whenever to provide internal actions logs, handy in case of troubleshooting           | false |

# Supported Formats

This version supports variables defied from plain text and json files.

The format will be determined by the file extensions : 
* JSON : .json
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

The action supports JSON files and handles nested properties declaration. Nested properties will be separated by an underscore ("_") before injection.

For instance, the following JSON content : 

```json
{ "build" : { 
    "version" : {
      "major" : "1",
      "minor" : "0",
      "patch" : "42"
    }
}}
```
will inject the following variables : 

```
build_version_major=1
build_version_minor=0
build_version_patch=42
```

### Known issues

Note that there are a couple of caveats in the structured parsing arrising with JSON format.

To start with the parser can only process *fully compliant JSON object declarations* ( i.e : { "K" : "V" } ) and won't be able to correctly process JSON payloads that declare an array of objects, such as : 

```json
{ [ {"build" : "always" } , { "tag" : "latest" } ] }
```

Moreover the prarser does not fully support list values, such as : 

```json
{ "envs" : [ "dev" , "test", "prod "]}
```

In the current state, the above mentionned payload will create the following vars : 

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

All usages are illustrated in the integration tests implemented in the main action workflow file [buildtest.yaml](.github/workflows/buildtest.yml). 

Here is a summary of the usage illustrations : 

| Use Case                 | Description            | Link |
| ------------------------ | ---------------------- |------|
| Single file | Imports all variables from the specified file | [view](.github/workflows/buildtest.yml?plain=1#L63-L67) |
| Multiple files | Imports all variables from the speficied file set | [view](.github/workflows/buildtest.yml?plain=1#L77-L82) |
| Prevent Override | Prevent overriding of variables already defined in the workflow file  | [view](.github/workflows/buildtest.yml?plain=1#L123-L128) |



# timefileChecker
Periodically writes timestamp to file allowing readyness probe to check if timestamp is current. Is to be used as a git submodule. 

## Requirements

Requires python and git to be used in the base project.

## Install and information

This tool is meant to be used from within another python based project. 
Therefore you should add this tool as a submodule to your git project in the base git directory using 

```console
git submodule add https://github.com/Sokrates1989/timeFileChecker.git
```

See https://git-scm.com/book/en/v2/Git-Tools-Submodules

## Preparation for usage

### Edit config

If you only have to use one state check for your tool (common):
Rename config.txt.template to config.txt

If your tool consists of multiple parts that each require an individual state check:
Rename config.txt.multiple_checks_template to config.txt

```
root
├── yourCodeBase
│   ├── file_to_import_tool_from.py
│   └── ..
├── timeFileChecker
│   ├── config.txt
│   ├── config.txt.template
│   ├── config.txt.multiple_checks_template
│   └── ..
└── ..
```


### Add the install directory to your python imports 

```python
# Import submodules.
# Insert path to submodules to allow importing them.
import os
import sys
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "path/",  "to/", "timeFileChecker"))
```

If your code structure is like below and you want to import this tool from file_to_import_tool_from.py, you may use the snippet below the folder structure example.

```
root
├── yourCodeBase
│   ├── file_to_import_tool_from.py
│   └── ..
├── timeFileChecker
└── ..
```

```python
# Import submodules.
# Insert path to submodules to allow importing them.
import os
import sys
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "../", "timeFileChecker"))
```


### Import the tool 

```python
# Import timeFileChecker.
import timeFileChecker as TimeFileChecker
```


## If you have a dev/live implementation

if you go live for the first time, you might have to remove submodule once and delete the submodule directory manually

```
git rm -r --cached timeFileChecker
```

remeber to also delete the directory timeFileChecker, then readd submodule as done in ##Install and information

```
git submodule add https://github.com/Sokrates1989/timeFileChecker.git
```



## Usage

### Start Writing TimeFile

This will run on a seperate Thread will your tool is running and send frequent pings to to server to tell it, that the tool is working.

If you only have to use one state check for your tool (common):

```python
timeFileChecker = TimeFileChecker.TimeFileChecker()
timeFileChecker.start()
```


### Check readyness of tool

Call the isToolReady.sh shell script 

```bash
sh path/to/isToolReady.sh
```

This script will check if the timestamp written is current.
The script will exit normally if the tool is running.
If the timestamp is older than the amount specified in the config, this script will exit in an unhealthy condition to allow kubernetes readyness probe to work properly.

### Implement Kubernetes readyness probe



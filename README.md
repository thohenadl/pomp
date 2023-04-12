<p align="center">
    <img src="https://img.shields.io/badge/Python-3.8 (x64)-blue?style=flat&labelColor=3776AB&color=3776AB&logo=python&logoColor=white" /></a>
</p>

# POMP
by @thohenadl

## Part of manual Processes
This repository contains the functionality described in Hohenadl et al´s paper on "POMP: Parts of manual Processes". The POMP-taxonomy allows clustering user interactions in user interface/interaction logs to be clustered into six categories:

* Open action
* Navigate action
* Transform action
* Transfer action
* Conclude action
* Close action

There can be empty actions as well. These are not required for the task execution in the manual process.

This projects provides currently one functions:
* Tagging equal actions in a UI-log
    * An equal action is defined as the same user interaction (e.g. mouse-click) on the same context attributes

A future research area is to use Levensthein-Distance:
* Clustering on Levensthein-Distance measure
    * The actions in the UI-log can be clustered based on the Levensthein-distance measure and the clusteres can be tagged


## How to Use
### Preliminary Work
- Clone the repository.
- Install **project** dependencies

  ```bash
  pip3 install -r requirements.txt
  ```

[Python](https://www.python.org/downloads/) ≥ 3.7 (_64bit_) is required.

### File Preperation
1. Set file to be tagged with POMP categories:
    * Go to folder "logs > pompTagged"
    * Add your file without a column for the "pomp_dim"
2. Store files that should be tagged
    * Go to folder "logs > uilogs"
    * Place all files that should be tagged based on the file in 1.

### Execution
Run the script or start the application with 

```bash
python main.py
```

## Support functionallity
There are two support functions in the project:

+ stats.py: Running stats.py generates an XML file with the generic stats about all files in the uilogs folder

  ```bash
  python stats.py
  ```

+ concat.py: Concat several UI logs into a single log file with a Case ID identifier per File
    + Adjust the 'file_path' parameter to a folder
    + Run the concat.py:
        ```bash
        python concat.py
        ```

## Examples
Show some examples of the project in action.

## Contribution
Guidelines on how to contribute to the project.

## License
Please refer to LICENSE file.
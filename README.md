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

This projects provides two functions:
* Tagging equal actions in a UI-log
    * An equal action is defined as the same user interaction (e.g. mouse-click) on the same context attributes
* Clustering on Levensthein-Distance measure
    * The actions in the UI-log can be clustered based on the Levensthein-distance measure and the clusteres can be tagged

## Requirements
The reuquirements are stored in the requirements.txt file.

## How to Use
### Preliminary Work
Clone the repository.
Install the required dependencies

'pip install -r requirements.txt'

### File Preperation
1. Set file to be tagged with POMP categories:
    * Go to folder "logs > pompTagged"
    * Add your file without a column for the "pomp_dim"
2. Store files that should be tagged
    * Go to folder "logs > uilogs"
    * Place all files that should be tagged based on the file in 1.

### Execution
Run the script or start the application with 'python main.py'
Detailed instructions on how to use the project (if necessary).

## Examples
Show some examples of the project in action.

## Contribution
Guidelines on how to contribute to the project.

## License
Please refer to LICENSE file.

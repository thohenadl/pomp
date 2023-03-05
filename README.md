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
List of required libraries or dependencies
Any other information needed to run the project

## How to Use
Clone the repository.
Install the required dependencies.
Run the script or start the application.
Detailed instructions on how to use the project (if necessary).

## Examples
Show some examples of the project in action.

## Contribution
Guidelines on how to contribute to the project.

## License
plese refer to LICENSE file.
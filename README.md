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

This projects provides currently one function:
* Tagging equal actions in a UI-log
    * An equal action is defined as the same user interaction (e.g. mouse-click) on the same context attributes

For future releases we intend to implement a user action distance measure:
* Clustering on Levensthein-Distance measure
    * The actions in the UI-log can be clustered based on the Levensthein-distance measure and the clusteres can be tagged

## Manual
We have created a detailed manual to use the file.
Please have a look at the POMP_Tagging_User_Manual.pdf

## Requirements
The requirements are stored in the requirements.txt file.

## How to Use
### Preliminary Work
Clone the repository.
Install the required dependencies.

'pip install -r requirements.txt'

### File Preperation
1. Set file to be tagged with POMP categories:
    * Go to folder "logs > pompTagged"
    * Add your file with or without a column for the "pomp_dim"
2. Store files that should be tagged
    * Go to folder "logs > uilogs"
    * Place all files that should be tagged based on the file in 1.

### Execution
Run the script or start the application with 'python main.py'
Detailed instructions on how to use the project (if necessary).

## Running Example Log
We provide a real-life use case log for testing and using the POMP tagging tool.
These example logs contain various remittance/banking transaction recordings using the [smartRPA](https://github.com/bpm-diag/smartRPA/tree/action_logger) recording tool.

The user interaction logs contain the login into a demo banking account, the selection of the deposit account, and the filling of the transaction with TAN confirmation.
The logs are available in the 'logs\banking' folder.

## Contribution
Open Contributions: We invite all users, regardless of their background or experience, to contribute to our project. Your unique perspectives and skills can greatly enhance our research. Feel free to explore, suggest improvements, and submit your own code.

Issue Tracker: Before starting any work, please check the repository's issue tracker. It contains a list of tasks, bugs, and ongoing discussions. If you find an issue that interests you, please comment on it to express your intent to work on it. If you have a new idea or find a bug that hasn't been reported yet, create a new issue.

Branching and Pull Requests: When making changes to the project, create a new branch with a descriptive name that reflects the purpose of your work. This helps us track changes and review contributions more easily. Submit a pull request when you are ready for your changes to be reviewed and merged into the main branch.

Code Documentation: Well-documented code is essential for the longevity and maintainability of our project. Please ensure that your contributions are accompanied by comprehensive documentation. This includes comments within the code, as well as clear explanations in the project's README file or relevant documentation files. Documenting your code will greatly assist other contributors in understanding and building upon your work.

## License
Please refer to LICENSE file.

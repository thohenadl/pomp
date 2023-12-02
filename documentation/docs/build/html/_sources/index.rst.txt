.. pomp documentation master file, created by
   sphinx-quickstart on Sat Dec  2 12:43:36 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pomp's documentation!
================================

**POMP** (Parts of manual processes) is a Python helper tool for task mining that
creates tagged data files for equal manual actions in user interaction logs.
It does allow simple tagging for multiple equal actions in a task mining log.

Identified Actions
------------------

* Open: Opening of applications or windows within an application
* Navigate: Navigation to an already open application or window
* Transform: Change of GUI elements, e.g. activating, selecting, or typing content
* Transfer: Copying content into the clipboard
* Conclude: Clicking a button after changing content on a page, e.g. sending a form or confirming a selection
* Close: Clsoing an application window
* Empty: Actions changing nothing on screen, e.h. Clicking on the background of an already active window

.. note::

   This project is under active development.

Contents
--------
.. toctree::

   usage

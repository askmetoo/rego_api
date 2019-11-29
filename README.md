# rego_api
Rego is a business workflow engine based on SpiffWorkflow that parses Camunda BPMN files and provides an API to drive a web interface.

Right now this is A VERY SIMPLE BPMN diagram that has a user task where they 
provide a type of fact (either cat, norris, or buzzword) and then gets the
fact from one of a set of open apis.  Printing the fact out to the command line.

## Getting Started
```bash
pip install -r requirements.txt
python fact_runner.py
```
Based on the from defined in the BPMN Model, you will be asked a question.
you will given a set of options.  It will then run a script that will look for
the selected value and execute an API call to get the fact back, and print it.


## TODO:
SpiffExtensions should likely be factored out into a library that other
systems will use to load diagrams and provide apis.  This directory contains
custom implementations of BPMN parsers and Tasks that can take advantage
of Camunda's custom tags within BPMN.


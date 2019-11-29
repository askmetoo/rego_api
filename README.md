# rego_api
Rego is a business workflow engine based on SpiffWorkflow that parses Camunda BPMN files and provides an API to drive a web interface.

Right now this is A VERY SIMPLE BPMN diagram that has a user task where they 
provide a type of fact (either cat, norris, or buzzword) and then gets the
fact from one of a set of open apis.  Printing the fact out to the command line.

## Getting Started
```bash
pip install -r requirements.txt
python FactCommandLine.py
```

## You can execute the script by typing 
```
> next         // Runs all tasks from the diagram
> type cat     // sets the type of fact to cat
> next         // Runs the final task which should print out the fact.
```

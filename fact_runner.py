from SpiffWorkflow.bpmn.workflow import BpmnWorkflow

from SpiffExtensions.Camunda.UserTask import UserTask
from SpiffExtensions.Camunda.BpmnSerializer import BpmnSerializer
from SpiffExtensions.CustomBpmnScriptEngine import CustomBpmnScriptEngine


def main():
    print("Loading BPMN Specification.")
    spec = bpmn_diagram_to_spec('bpmn/')

    print ("Creating a new workflow based on the specification.")
    script_eginine = CustomBpmnScriptEngine()
    workflow = BpmnWorkflow(spec, script_engine=script_eginine)

    print ("Running automated tasks.")
    workflow.do_engine_steps()

    while not workflow.is_completed():
        workflow.do_engine_steps()
        ready_tasks = workflow.get_ready_user_tasks()
        while len(ready_tasks) > 0:
            for task in ready_tasks:
                if isinstance(task.task_spec, UserTask):
                    show_form(task)
                    workflow.complete_next()
                else:
                    raise("Unown Ready Task.")
            workflow.do_engine_steps()
            ready_tasks = workflow.get_ready_user_tasks()


def show_form(task):
    model = {}
    form = task.task_spec.form
    for field in form.fields:
        print("Please complete the following questions:")
        prompt = field.label + "? (Options: " + ', '.join([str(option.id) for option in field.options]) + ") ? "
        model[form.key + "." + field.id] = input(prompt)
    task.data = model


def bpmn_diagram_to_spec(file_path):
    """This loads up all BPMN diagrams in the BPMN folder."""
    workflowSpec = BpmnSerializer().deserialize_workflow_spec(file_path)
    return workflowSpec


if __name__ == "__main__":
    main()

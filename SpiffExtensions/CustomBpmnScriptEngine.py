from SpiffWorkflow.bpmn.BpmnScriptEngine import BpmnScriptEngine


class CustomBpmnScriptEngine(BpmnScriptEngine):
    """This is a custom script processor that can be easily injected into Spiff Workflow.
    Rather than execute arbitrary code, this assumes the script references a fully qualified python class
    such as myapp.RandomFact. """

    def execute(self, task, script, **kwargs):
        """
        Assume that the script read in from the BPMN file is a fully qualified python class. Instantiate
        that class, pass in any data available to the current task so that it might act on it.
        Assume that the class implements the "do_task" method.

        This allows us to reference custom code from the BPMN diagram.
        """
        module_name = script
        class_name = module_name.split(".")[-1]
        mod = __import__(script, fromlist=[class_name])
        klass = getattr(mod, class_name)
        klass().do_task(task.data)

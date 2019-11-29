from cmd import Cmd
from io import BytesIO
from xml.etree import ElementTree

from SpiffWorkflow.bpmn.serializer.BpmnSerializer import BpmnSerializer
from SpiffWorkflow.bpmn.serializer.Packager import Packager
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow

from SpiffExtensions.CustomBpmnScriptEngine import CustomBpmnScriptEngine
from model.fact import Fact


class InMemoryPackager(Packager):
    """
    Creates spiff's wf packages on the fly.
    Much of this is kindly borrowed from Denny Weinberg https://github.com/labsolutionlu/bpmn_dmn
    """

    @classmethod
    def package_in_memory(cls, workflow_name, workflow_files, editor):
        """
        Generates wf packages from workflow diagrams.
        """
        s = BytesIO()
        p = cls(s, workflow_name, meta_data=[], editor=editor)
        p.add_bpmn_files_by_glob(workflow_files)
        p.create_package()
        return s.getvalue()


class MyPrompt(Cmd):

    def bpmn_diagram_to_spec(self, file_path):
        """Basically, pre-parse the xml and figure out what the primary process id is (where do you start?),
        and what editor created the file. Then load the full file into a byte array and generate a Spiff
        Workflow spec from that file. This describes a full process in abstract.  We'll later instantiate the
        spec and run it through to it's completion."""
        packager = InMemoryPackager
        etr_root = ElementTree.parse(file_path).getroot() # definitions
        process_id = self.__getWorkflowProcessID(ETRroot=etr_root)
        editor = etr_root.attrib['exporter'] # the program that generated the BPMN Diagram
        package = packager.package_in_memory(process_id, file_path, editor)
        workflowSpec = BpmnSerializer().deserialize_workflow_spec(package)
        return workflowSpec

    @staticmethod
    def __getWorkflowProcessID(ETRroot):
        processElements = []
        for child in ETRroot:
            if child.tag.endswith('process') and child.attrib.get('isExecutable', False):
                processElements.append(child)

        if len(processElements) == 0:
            raise Exception('No executable process tag found')

        if len(processElements) > 1:
            raise Exception('Multiple executable processes tags found')

        return processElements[0].attrib['id']

    def __init__(self):
        super().__init__()

        spec = self.bpmn_diagram_to_spec('bpmn/random_fact.bpmn')
        script_eginine = CustomBpmnScriptEngine()

        self.workflow = BpmnWorkflow(spec, script_engine=script_eginine)

        self.workflow.debug = False

    @staticmethod
    def __getWorkflowProcessID(ETRroot):
        processElements = []
        for child in ETRroot:
            if child.tag.endswith('process') and child.attrib.get('isExecutable', False):
                processElements.append(child)

        if len(processElements) == 0:
            raise Exception('No executable process tag found')

        if len(processElements) > 1:
            raise Exception('Multiple executable processes tags found')

        return processElements[0].attrib['id']

    def do_quit(self, args):
        """Quits the program."""
        print("Quitting.")
        raise SystemExit

    def do_next(self, args):
        """Does every automatic task, and the responds back with a recommendation """
        self.workflow.do_engine_steps()
        ready_tasks = self.workflow.get_ready_user_tasks()
        if len(ready_tasks) == 1:
            print("The next task to complete is " + ready_tasks[0].get_name())
        if len(ready_tasks) > 1:
            print("You have multiple options to complete next!")
            for task in ready_tasks:
                print("\t" + str(task.id) + " : " + str(task.get_name()))

    def do_type(self, args):
        """Set the type of fact"""
        tasks = self.workflow.get_ready_user_tasks()
        data = {}
        data["fact"] = Fact(fact_type=args)
        print("You answered " + args)
        if len(tasks) == 1:
            tasks[0].set_data(**data)
            self.workflow.complete_next()


if __name__ == '__main__':
    prompt = MyPrompt()
    prompt.cmdloop('Starting prompt...')

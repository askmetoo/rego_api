from SpiffWorkflow.bpmn.parser.BpmnParser import BpmnParser, full_tag

from SpiffExtensions.Camunda.UserTask import UserTask
from SpiffExtensions.Camunda.UserTaskParser import UserTaskParser


class BpmnParser(BpmnParser):
    OVERRIDE_PARSER_CLASSES = {
        full_tag('userTask'): (UserTaskParser, UserTask),
    }



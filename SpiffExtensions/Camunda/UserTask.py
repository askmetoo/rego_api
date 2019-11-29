# -*- coding: utf-8 -*-
from __future__ import division

from SpiffWorkflow.bpmn.specs.BpmnSpecMixin import BpmnSpecMixin
from SpiffWorkflow.specs import Simple


class UserTask(Simple, BpmnSpecMixin):

    print("Custom User Task imported")

    """
    Task Spec for a bpmn:userTask node.
    """

    def _on_trigger(self, my_task):
        pass

    def is_engine_task(self):
        return False

import json
import unittest

from SpiffExtensions.Camunda.BpmnSerializer import BpmnSerializer
from tests.base_test import BaseTest


class TestBpmnSerializer(BaseTest, unittest.TestCase):

    def test_truthyness(self):
        self.assertTrue(True)

    def test_bpmnSerializer(self):
        serializer = BpmnSerializer()
        spec = serializer.deserialize_workflow_spec("../bpmn")
        self.assertIsNotNone(spec)

    def test_deserialize_bpmn_finds_camunda_form_with_options(self):
        serializer = BpmnSerializer()
        spec = serializer.deserialize_workflow_spec("../bpmn")
        form = spec.task_specs['Task_User_Select_Type'].form
        self.assertIsNotNone(form)
        self.assertEquals("Fact", form.key)
        self.assertEquals(1, len(form.fields))
        self.assertEquals("type", form.fields[0].id)
        self.assertEquals(3, len(form.fields[0].options))

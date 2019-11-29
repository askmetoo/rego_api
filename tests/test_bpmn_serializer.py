import json
import unittest

from SpiffExtensions.Camunda.BpmnSerializer import BpmnSerializer
from tests.base_test import BaseTest


class TestBpmnSerializer(BaseTest, unittest.TestCase):

    def test_truthyness(self):
        self.assertTrue(True)

    def test_bpmnSerializer(self):
        serializer = BpmnSerializer()
        serializer.deserialize_workflow_spec("../bpmn")
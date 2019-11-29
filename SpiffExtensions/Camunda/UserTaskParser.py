from SpiffWorkflow.bpmn.parser.TaskParser import TaskParser, xpath_eval

from SpiffExtensions.Camunda.UserTask import Form, EnumFormField, FormField

CAMUNDA_MODEL_NS = 'http://camunda.org/schema/1.0/bpmn'


class UserTaskParser(TaskParser):
    """
        The Camunda Editor will allow the creation of form definitions within a user task.
        This will pick up that data and parse it, making it available for processing later.
<bpmn:userTask id="Task_User_Select_Type" name="Set Type" camunda:formKey="Fact">
      <bpmn:extensionElements>
        <camunda:formData>
          <camunda:formField id="type" label="Type" type="enum" defaultValue="cat">
            <camunda:value id="norris" name="Chuck Norris" />
            <camunda:value id="cat" name="Cat Fact" />
            <camunda:value id="buzzword" name="Business Buzzword" />
          </camunda:formField>
        </camunda:formData>
        <camunda:inputOutput>
          <camunda:outputParameter name="Output_2958k2h" />
        </camunda:inputOutput>
        <camunda:properties>
          <camunda:property name="type" value="string" />
        </camunda:properties>
      </bpmn:extensionElements>
      <bpmn:incoming>SequenceFlow_0ik56h0</bpmn:incoming>
      <bpmn:outgoing>SequenceFlow_1wl4cli</bpmn:outgoing>
    </bpmn:userTask>
    """

    def __init__(self, process_parser, spec_class, node):
        super().__init__(process_parser, spec_class, node)
        self.xpath = xpath_eval(node,extra_ns={'camunda':CAMUNDA_MODEL_NS})

    """
    Base class for parsing User Tasks
    """
    print("Custom User Task Parser for Camunda Located")
    pass

    def create_task(self):
        form = self.get_form()
        return self.spec_class(self.spec, self.get_task_spec_name(), form,
                               description=self.node.get('name', None))

    def get_form(self):
        """Camunda provides a simple form builder, this will extract the details from that form
        and construct a form model from it. """
        form = Form()
        form.key = self.node.attrib['{' + CAMUNDA_MODEL_NS + '}formKey']
        for xml_field in self.xpath('.//camunda:formData/camunda:formField'):
            if xml_field.get('type') == 'enum':
                field = self.get_enum_field(xml_field)
            else:
                field = FormField()
            field.id = xml_field.get('id')
            field.type = xml_field.get('type')
            field.label = xml_field.get('label')
            field.default_value = xml_field.get('defaultValue')
            form.add_field(field)
            print(xml_field.text)
        return form

    def get_enum_field(self, xml_field):
        field = EnumFormField()
        for option in xml_field:
            field.add_option(option.get('id'), option.get('name'))
        return field



from datetime import datetime
from enum import Enum

import yaml


class InputType(Enum):
    ''''''
    String = 'String'
    Integer = 'Integer'
    Decimal = 'Decimal'


class OutputType(Enum):
    ''''''
    String = 'String'
    Integer = 'Integer'
    Decimal = 'Decimal'
    Date = 'Date'


class RuleType(Enum):
    ''''''
    Static = 'Static'
    Calculation = 'Calculation'


class SourceNotFound(Exception):
    '''Custom Exception for when expected data could not be found'''
    pass


class Rule:
    '''
    Class representation of a Rule

    ...

    Attributes
    ----------
    source : str
        the key to use to pull from the data source
    target : str
        the key to use for the resulting data set
    type : RuleType
        the rule type
    input_type: InputType
        the data type the rule should read the value from the source as
    output_type : OutputType
        the python data type you want the value to conform to
    operations : list
        the operations you want performed on the variable
    '''
    def __init__(self, source=None, target=None, type=RuleType.Static, input_type=InputType.String, output_type=OutputType.String, operations=[]):
        self.source = source
        self.target = target
        self.type = type
        self.input_type = input_type
        self.output_type = output_type
        self.operations = operations

    def _value_as_output_type(self, value):
        ''''''
        if self.output_type == OutputType.Integer:
            return int(value)

        if self.output_type == OutputType.String:
            return str(value)

        if self.output_type == OutputType.Decimal:

            if type(value) is float:
                return value

            # Check for commas
            if type(value) is str:
                value = value.replace(',', '')

            return float(value)

        return value


    def _perform_operations(self, value):
        ''''''
        params = {'s': value}

        if self.output_type == OutputType.Date:
            params['datetime'] = datetime

        for operation in self.operations:
            value = eval(operation, params)

        return value

    def _fetch_value(self, key, data):
        if key in data:
            value = data[key]
            if self.input_type == InputType.Decimal or self.input_type == InputType.Integer:
                value = value.replace(',', '')
                value = int(value) if self.input_type == InputType.Integer else float(value)
            return value
        else:
            raise SourceNotFound

    def execute(self, data):
        '''Executes the rule on a given set of data

        Args:
            data (dict): A k,v representation of a csv row

        Returns:
            Tuple: A tuple with the first element being Rule.target, and with the second element being the type set by Rule.output_type

        Raises:
            SourceNotFound

            ValueError
        '''

        # value is going to just be self.source
        if self.type == RuleType.Static:
            value = self.source

        # fetch the value from self.source
        if self.type == RuleType.Calculation and type(self.source) is str:
            value = self._fetch_value(self.source, data)

        # fetch all of the values and store them in a list
        if self.type == RuleType.Calculation and type(self.source) is list:
            value = list(map(lambda k: self._fetch_value(k, data), self.source))

        value = self._perform_operations(value)

        return self.target, self._value_as_output_type(value)



    def as_dict(self):
        '''
        Returns:
            dict: A dictionary representation of the rule
        '''
        result = {
            'target': self.target,
            'type': self.type.value,
            'input_type': self.input_type.value,
            'output_type': self.output_type.value,
            'source': self.source,
            'operations': self.operations
        }
        return result


def load_rules_from_yaml(file_name):
    '''Generates a list of rules given a yaml configuration.

    Args:
        file_name (str): The file path of the file to use.

    Returns:
        list: A list of rules based on the given configuration.
    '''

    file = open(file_name)
    definition = yaml.full_load(file)
    file.close()

    rules = []
    for rule in definition['rules']:
        target = rule['target']
        rule_type = RuleType(rule['type'])
        input_type = InputType(rule['input_type'])
        output_type = OutputType(rule['output_type'])
        source = rule['source']
        operations = rule['operations'] if 'operations' in rule else []

        rule = Rule(
            source=source,
            target=target,
            type=rule_type,
            input_type=input_type,
            output_type=output_type,
            operations=operations
        )
        rules.append(rule)

    return rules

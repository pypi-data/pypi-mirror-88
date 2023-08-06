from decimal import Decimal
from datetime import datetime
from enum import Enum

import yaml


class OutputType(Enum):
    String = "String"
    Integer = "Integer"
    Decimal = "Decimal"
    Date = "Date"


class SourceNotFound(Exception):
    pass


class Rule:
    """
    Class representation of a Rule

    ...

    Attributes
    ----------
    source : str
        the key to use to pull from the data source
    target : str
        the key to use for the resulting data set
    output_type : OutputType
        the python data type you want the value to conform to
    """
    def __init__(self, source=None, target=None, output_type=OutputType.String, operations=None):
        self.source = source
        self.target = target
        self.output_type = output_type
        self.operations = operations

    def _value_as_output_type(self, value):
        if self.output_type == OutputType.Integer:
            return int(value)
        if self.output_type == OutputType.String:
            return str(value)
        if self.output_type == OutputType.Decimal:
            if type(value) is Decimal:
                return value
            if type(value) is str:
                value = value.replace(',', '')
            return Decimal(value)

    def execute(self, data):
        '''Implemented in subclasses'''
        pass # pragma: no cover

    def as_dict(self):
        '''Return a Dictionary representation of the rule'''
        result = {
            'target': self.target,
            'to_type': self.output_type.value,
            'source': self.source,
            'operations': self.operations
        }
        return result


class StaticRule(Rule):
    """
    Use Case: Static value for every row
    """
    def execute(self, data):
        """Returns the static value with self.target

        Args:
            data (dict): The data to perform to rule on.

        Returns:
            str, result: A k,v pair representing the target, and the retrieved/calculated value

        Raises:
            SourceNotFound: If the source cannot be found in the given data.
        """
        """Returns self.target, self.value as a key, value pair with self.value being cast to self.output_type"""
        return self.target, self._value_as_output_type(self.source)

    def as_dict(self):
        result = super().as_dict()
        result['type'] = 'static'
        return result


class SingleSourceRule(Rule):
    """
    Use Case: Extract value from column, place in new column
    """

    def execute(self, data):
        """Attempts to retrieve self.source from data.

        Args:
            data (dict): The data to perform to rule on.

        Returns:
            str, result: A k,v pair representing the target, and the retrieved/calculated value

        Raises:
            SourceNotFound: If the source cannot be found in the given data.
        """
        if self.source in data:
            value = data[self.source]
            if self.operations:
                for operation in self.operations:
                    value = eval(operation, {'s': value})
            return self.target, self._value_as_output_type(value)
        else:
            raise SourceNotFound

    def as_dict(self):
        result = super().as_dict()
        result['type'] = 'single'
        return result

class CalculationRule(Rule):
    """
    Use Case: Perform arithmetic calculations with values from columns
    """

    def execute(self, data):
        """Attempts to retrieve all of the values in self.source, then performs the calculations defined in self.operations.

        Args:
            data (dict): The data to perform to rule on.

        Returns:
            str, Decimal: A k,v pair representing the target, and the retrieved/calculated value

        Raises:
            SourceNotFound: If the any of the keys in self.source cannot be found in the given data.
        """
        values = []
        for key in self.source:
            if key in data:
                v = data[key]
                v = v.replace(',', '')
                v = Decimal(v)
                values.append(v)
            else:
                raise SourceNotFound
        value = eval(self.operations[0], {'s': values})
        return self.target, self._value_as_output_type(value)

    def as_dict(self):
        result = super().as_dict()
        result['type'] = 'multiple'
        return result


class DateRule(Rule):
    """
    Use Case: Gather date part values from multiple columns, generate date value
    """

    def execute(self, data):
        """Attempts to retrieve day, month, and year values from data,

        Args:
            data (dict): The data to perform to rule on.

        Returns:
            str, datetime: A k,v pair representing the target, and the retrieved/calculated value

        Raises:
            SourceNotFound: If the source cannot be found in the given data.
        """
        day_source = self.source['day']
        month_source = self.source['month']
        year_source = self.source['year']

        if day_source in data and month_source in data and year_source in data:
            day = int(data[day_source])
            month = int(data[month_source])
            year = int(data[year_source])
            return self.target, datetime(year, month, day)
        else:
            raise SourceNotFound

    def as_dict(self):
        result = super().as_dict()
        result['type'] = 'multiple'
        return result


def load_rules_from_yaml(file_name):
    """Generates a list of rules given a yaml configuration.

    Args:
        file_name (str): The file path of the file to use.

    Returns:
        list: A list of rules based on the given configuration.
    """
    file = open(file_name)
    definition = yaml.full_load(file)
    file.close()
    rules = []
    for rule in definition['rules']:
        target = rule['target']
        rule_type = rule['type']
        output_type = OutputType(rule['to_type'])
        source = rule['source']
        operations = rule['operations'] if 'operations' in rule else None

        if rule_type == 'multiple':
            if output_type == OutputType.Date:
                date_rule = DateRule(
                    source={
                        'day': source['day'],
                        'month': source['month'],
                        'year': source['year']
                    },
                    target=target,
                    output_type=output_type,
                    operations=operations
                )
                rules.append(date_rule)

            if output_type == OutputType.Decimal:
                calculation_rule = CalculationRule(
                    source=source,
                    target=target,
                    output_type=output_type,
                    operations=operations
                )
                rules.append(calculation_rule)

        elif rule_type == 'single':
            single_source_rule = SingleSourceRule(
                source=source,
                target=target,
                output_type=output_type,
                operations=operations
            )
            rules.append(single_source_rule)

        elif rule_type == 'static':
            static_rule = StaticRule(
                source=source,
                target=target,
                output_type=output_type,
                operations=operations
            )
            rules.append(static_rule)

        else:
            print('Unknown rule definition')
            print('Target: {}\n Type: {}\n Output Type: {}\n Source: {}'.format(target, rule_type, output_type, source))

    return rules


def export_rules_as_yaml(rules):
    """Converts a set of rules into a yaml configuration.

    Args:
        rules (list): The list of rules to convert.

    Returns:
        str: The yaml representation of the given rules.
    """
    rule_defs = []
    for rule in rules:
        rule_defs.append(rule.as_dict())
    return yaml.dump({'rules': rule_defs})

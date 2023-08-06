import yaml
from decimal import (Decimal)
from datetime import datetime


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
    output_type : str
        the python data type you want the value to conform to

    Methods
    -------
    execute(data)
        Implemented in subclasses

    as_dict()
        Return a Dictionary representation of the rule

    _value_as_output_type(value)
        Attempts to cast value to self.output_type and return
    """
    def __init__(self, source=None, target=None, output_type='String'):
        self.source = source
        self.target = target
        self.output_type = output_type

    def _value_as_output_type(self, value):
        if self.output_type == 'Integer':
            return int(value)
        if self.output_type == 'String':
            return str(value)
        if self.output_type == 'Decimal':
            return Decimal(value.replace(',', ''))

    def execute(self, data):
        # Implemented in sub classes
        pass

    def as_dict(self):
        result = {
            'target': self.target,
            'to_type': self.output_type,
            'source': self.source
        }
        return result


class StaticRule(Rule):
    """
    Use Case: Static value for every row
    """
    def execute(self, data):
        """Returns self.target, self.value as a key, value pair with self.value being cast to self.output_type"""
        return self.target, self._value_as_output_type(self.source)

    def as_dict(self):
        result = super().as_dict()
        result['operation'] = 'static'
        return result


class SingleSourceRule(Rule):
    """
    Use Case: Extract value from column, place in new column
    """
    def execute(self, data):
        """Attempts to retrieve self.source from data,
        then returns self.target, and the value as a key, value pair.
        If self.source is not in the provided data, raises SourceNotFound
        """
        if self.source in data:
            value = data[self.source]
            return self.target, self._value_as_output_type(value)
        else:
            raise SourceNotFound

    def as_dict(self):
        result = super().as_dict()
        result['operation'] = 'extract'
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
        result['operation'] = 'extract'
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
        operation = rule['operation']
        output_type = rule['to_type']
        source = rule['source']

        if operation == 'extract' and output_type == 'Date':
            date_rule = DateRule(
                source={
                    'day': source['day'],
                    'month': source['month'],
                    'year': source['year']
                },
                target=target,
                output_type='Date'
            )
            rules.append(date_rule)

        elif operation == 'extract' and output_type != 'Date':
            single_source_rule = SingleSourceRule(
                source=source,
                target=target,
                output_type=output_type
            )
            rules.append(single_source_rule)

        elif operation == 'static':
            static_rule = StaticRule(
                source=source,
                target=target,
                output_type=output_type
            )
            rules.append(static_rule)

        else:
            print('Unknown rule definition')
            print('Target: {}\n Operation: {}\n Output Type: {}\n Source: {}'.format(target, operation, output_type, source))

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

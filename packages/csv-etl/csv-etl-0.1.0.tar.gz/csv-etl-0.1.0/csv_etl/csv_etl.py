import io
import csv
import json
from datetime import datetime


ERROR_MSG_TEMPLATE = "Error executing:\n\tRule: {}\n{}:\n\t{}"


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d')

        return json.JSONEncoder.default(self, o)


class CSVConverter:
    """Essentially a wrapper around a set of rules"""

    def __init__(self, rules):
        self.rules = rules

    def _write_to_outfile(self, data, outfile):
        """Internal method to write converted results to outfile.

        Args:
            data (str/dict): The data to be written.
            outfile (str): The file path to write the result to.

        """
        file = open(outfile, 'w')
        file.write(str(data))
        file.close()

    def _convert_to_csv(self, data):
        """Internal method to convert json data into csv data.

        Args:
            data (dict): The data to be converted.

        """
        csv_result = io.StringIO()
        field_names = []
        for rule in self.rules:
            field_names.append(rule.target)
        writer = csv.DictWriter(csv_result, field_names)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
        return csv_result.getvalue()

    def convert(self, csv_file, to=None, outfile=None):
        """Example function with types documented in the docstring.

        Args:
            csv_file (str): The file path of the csv file to convert.
            to (str): What to return the output as, either `csv` or `json`. Default `json`.
            outfile (str): Optional - The file path to write the result to.

        Returns:
            str/dict: Depending on to `to parameter`
        """
        result = []
        source_file = open(csv_file)
        reader = csv.DictReader(source_file)

        for row in reader:
            row_result = {}
            for rule in self.rules:
                try:
                    k, v = rule.execute(row)
                    row_result[k] = v
                except SourceNotFound:
                    error_msg = ERROR_MSG_TEMPLATE.format(str(rule.as_dict()), "Unable to retrieve source data from", str(row))
                    print(error_msg)
                    row_result[rule.target] = ""
                except ValueError as e:
                    error_msg = ERROR_MSG_TEMPLATE.format(str(rule.as_dict()), "Unable to convert data type for", str(row))
                    print(error_msg)
                    row_result[rule.target] = ""

            result.append(row_result)

        if to == 'csv':
            result = self._convert_to_csv(result)

        if to == 'json':
            result = json.dumps(result, cls=CustomEncoder)

        if outfile:
            self._write_to_outfile(result, outfile)

        source_file.close()
        return result

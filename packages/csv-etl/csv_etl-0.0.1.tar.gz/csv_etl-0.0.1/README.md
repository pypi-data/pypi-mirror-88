# csv-etl

A rules based approach to performing ETL operations on csv files.

## Installation

```bash
pip install csv-etl
```

## Quick Introduction

The goal of this project is to provide a re-usable way to perform ETL operations on csv files. This implementation takes a given row of data from a csv file and applies a set of rules to generate a new format of the data.
A rule knows three things

 - Where the original data is coming from (`source`)
 - Where the new data is going to (`target`)
 - The data type the new data is expected to conform to (`output_type`)
	 - `output_type` can be the following options and will result in the correlating python types
		 - `Integer` : `int`
		 - `Decimal` : `decimal.Decimal`
		 - `String` : `str`
		 - `Date` : `datetime.datetime`

The root `Rule` class in this library contains those three properties.

The `Rule` class is subclassed, and the subclasses are where the logic for extracting/modifying the data takes place.

The current `Rule` subclasses are

 - `StaticRule`
	 - Use Case: Static value for every row
 - `SingleSourceRule`
	 - Use Case: Extract value from source column, place in new target column
 - `DateRule`
	 - Use Case: Gather date part values from multiple columns, generate date value

## Usage

### With a config file
```python
from csv_etl.rules import load_rules_from_yaml
from csv_etl import CSVConverter

rules = load_rules_from_yaml("path/to/config/file")
csv_converter = CSVConverter(rules)
result = csv_converter.convert("path/to/csv/file")
```

Configuration examples [can be found here](https://github.com/winslowdibona/csv_converter/blob/master/examples/config)

The basic structure of the configuration file is:

```yaml
rules:
  -
    target: The new key
    operation: extract || static
    to_type: Integer || String || Decimal || Date
    source: Where to pull data from
```



### Creating rules programmatically

```python
from csv_etl.rules import (
  StaticRule,
  SingleSourceRule,
  DateRule
)
from csv_etl import CSVConverter

rules = [
  StaticRule(source='kg', target='Unit', output_type='String')
  SingleSourceRule(source='Order Number', target='OrderId', output_type='Integer'),
  DateRule(source={'day': 'Day', 'month': 'Month', 'year': 'Year'}, target='OrderDate', output_type='Date'),
]
csv_converter = CSVConverter(rules)
result = csv_converter.convert("path/to/csv_file")

# By default, the result is a json array. But you can receive is back as a csv string
result = csv_converter.convert("path/to/csv/file", to='csv')

# You can also write the result to a specified file
result = csv_converter.convert("path/to/csv/file", to='csv', outfile="path/to/outfile")
```


A step by step use case of this [can be found here](https://github.com/winslowdibona/csv_etl/blob/master/examples/OrderDataExample.md)


## Developing

### Make Commands
```bash
# run test suite
pytest
# generate test coverage
test-cov
# generate docs
docs
# build distribution files
build-dist
# run in docker container
play
```

## What Next?

### Expand on Date Rule

The current implementation of the `DateRule` is fairly rigid. It only covers the use case of there being day/month/year columns in the given csv. It also assumes the data values are numbers and not string representations of the months like `March`

This could be expanded upon to

 - Handle month strings
 - Handle different date formats
	 - YYYY-mm-dd
	 - mm-dd-YYYY
	 - dd-mm-YYYY

### Calculation Rules

Introducing a new `CalculationRule` that takes

 - a list of column names for its `source`
 - an `operation_type` (`"+"`, `"-"`, `"*"`, `"/"`)

When executed, the rule would gather the data, perform the calculation and assign it to the `target`.

### Better error handling

Currently the errors are just printed to the console. Might be nice to have an option to gather them and have them represented in the resulting data set somehow.

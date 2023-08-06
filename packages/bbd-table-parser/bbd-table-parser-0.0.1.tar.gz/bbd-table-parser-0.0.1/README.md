# Table Parser

Intended to be used with [pytest_bdd](https://pypi.org/project/pytest-bdd/) for parsing inline tables from str into dict

Example:
```gherkin
Given I have a thing
When I do stuff:
    | Heading | Other Heading |
    | to do   | Also          |
    | more    | Other         |
Then everything is great
```

```python
from pytest_bdd import when, parsers
from table_parser.table_parser import table_parser

@when(parsers.cfparse('I do stuff:\n{table}'))
def verify_date_from_request(table):
    table_dict = table_parser(table)
```
import re


MULTI_COLUMN_TABLE = r'\|.+\|.+\|'
SEPARATOR_WITH_LINE_END = r'\|\n'
SEPARATOR_WITH_WHITE_SPACE = r' \| '
SEPARATOR = r'\|'


def clean_line(line: str):
    split_line = []
    if re.search(MULTI_COLUMN_TABLE, line):
        for l in re.split(SEPARATOR_WITH_WHITE_SPACE, line.strip()):
            l = re.sub(SEPARATOR, '', l)
            l = l.strip()
            split_line.append(l)

        return split_line

    else:
        line = re.sub(SEPARATOR, '', line)
        line = line.strip()
        return line


def table_parser(table) -> dict:
    headers = None
    return_table = {}
    if re.search(MULTI_COLUMN_TABLE, table):
        rows = []
        for line in table.strip().splitlines():
            split_line = clean_line(line)
            if not headers:
                headers = split_line
            else:
                rows.append(split_line)
        for header in headers:
            row = []
            for l in rows:
                row.append(l[headers.index(header)])
            return_table[header] = row
    else:
        list_of_thing = []
        for line in re.split(SEPARATOR_WITH_LINE_END, table.strip()):
            line = clean_line(line)
            if not headers:
                headers = line
                return_table[headers] = []
            else:
                list_of_thing.append(line)
        return_table[headers] = list_of_thing
    return return_table


if __name__ == '__main__':
    text = """
    | cover artists     | writer  |
    | Joe Madureira     |   Joe Bean    |
    | Aron Lusen        |   Jane Bean   |
    | Humberto Ramos    |   Utah        |
    | Edgar Delgado     |   Orian       |
    | J. Scott Campbell |   Simon       |
    | Joe Quesada       |   Terry       |
    | Danny Miki        |   Brandon     |
    | Richard Isanove   |   Jason       |
    """

    text2 = """
    | cover artists     |
    | Joe Madureira     |
    | Aron Lusen        |
    | Humberto Ramos    |
    | Edgar Delgado     |
    | J. Scott Campbell |
    | Joe Quesada       |
    | Danny Miki        |
    | Richard Isanove   |
    """

    print(table_parser(text))
    print(table_parser(text2))

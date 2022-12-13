import csv
from typing import Dict, List

from loguru import logger

from utils import move_file, get_file_names
from db import create_db_objects, insert_into_db


def get_table_specs(selected_spec: str) -> List[Dict]:
    """Gets table specs for selected_spec.
    Returns a list of dicts with the following keys: column name, width, datatype."""

    file_specs = get_file_names('specs')
    file_spec = list(filter(lambda x: x.startswith(selected_spec), file_specs))

    if not file_spec or len(file_spec) > 1:
        raise ValueError(f'No spec or multiple spec found for {selected_spec}')

    file_spec = file_spec[0]

    logger.info(f'Using spec: {file_spec}')

    with open(f'specs/{file_spec}', 'r') as f:
        csv_reader = list(csv.DictReader(f))

    return csv_reader


def parse_csv_row(row: str, table_specs: List[Dict]) -> List[Dict]:
    """Parses a single row of the data file converting strings to the correct type."""

    type_map = {'TEXT': str, 'INTEGER': int, 'BOOLEAN': lambda x: bool(int(x))}

    start = 0
    parsed_row = []

    for column in table_specs:
        column_name = column['column name']
        column_width = int(column['width'])
        column_type = type_map[column['datatype']]

        value = row[start:start + column_width].strip()
        start += column_width

        data = {'column_name': column_name, 'column_value': column_type(value)}
        parsed_row.append(data)

    return parsed_row


def parse_csv(table_specs: List[Dict], file_name: str) -> List[Dict]:
    """Parses the data file.
    Returns a list of dicts with the following keys: column name, column value."""

    parsed_rows = []
    with open(f'data/{file_name}', 'r') as f:
        for row in f:
            parsed_rows.append(parse_csv_row(row, table_specs))

    logger.info(f'Parsed {len(parsed_rows)} data rows')
    logger.info(f'First row: {parsed_rows[0]}')

    return parsed_rows


def main():
    f_names = get_file_names('data')
    if len(f_names) == 0:
        logger.info('No files to process')
        return

    logger.info(f'Files to process: {len(f_names)}')
    for f in f_names:
        logger.info(f'Processing file: {f}')
        table_name = f.split('_')[0]
        table_specs = get_table_specs(table_name)
        parsed_rows = parse_csv(table_specs, f)

        objects_to_insert = create_db_objects(parsed_rows, table_specs, table_name)
        insert_into_db(objects_to_insert)
        logger.info(f'Moving file to processed folder')
        move_file(f)


if __name__ == '__main__':
    main()

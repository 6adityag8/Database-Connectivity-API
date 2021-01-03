from collections import defaultdict

from django.conf import settings
from rest_framework import status
from sqlalchemy import create_engine


def extract_info_from_request(request_data):
    """
    Extracts information from the incoming request's data.
    :param request_data: Dictionary containing incoming POST request's payload
    :return: Dictionary db_info which contains information passed in the POST request's payload
    """
    db_info = dict()
    db_info['database_name'] = request_data.get('database_name')
    db_info['table_name'] = request_data.get('data', {}).get('table_name')
    db_info['worksheet_id'] = request_data.get('data', {}).get('worksheet_id')

    # Collect all the columns from the select_list
    db_info['select_list'] = []
    for column_dict in request_data.get('data', {}).get('select_list', []):
        db_info['select_list'].append(column_dict.get('column'))
    db_info['select_list'] = list(filter(None, db_info['select_list']))

    # Collect columns in the aggregate list as a dictionary with
    # aggregate function as the key and columns list as the value
    db_info['aggregate'] = defaultdict(list)
    for aggregate_dict in request_data.get('data', {}).get('aggregate', []):
        db_info['aggregate'][aggregate_dict.get('type', '')].append(aggregate_dict.get('column'))
    db_info['aggregate'].pop('', None)

    # Collect all the columns from the group_by list
    db_info['groupby'] = []
    for groupby_dict in request_data.get('data', {}).get('groupby', []):
        db_info['groupby'].append(groupby_dict.get('column'))
    db_info['groupby'] = list(filter(None, db_info['groupby']))

    return db_info


def get_db_details(db_info):
    """
    Generates the SQL query and get the required details from the database.
    :param db_info: Dictionary containing information passed in the POST request's payload
    :return: A tuple of 3 elements containing the following information:
    db_columns: List of columns in the result set
    db_details: List of lists of the data in the result set
    error: A tuple containing error message and the error status code to be returned, if any error occurs
    """
    db_columns, db_details, err = [], [], None
    if not db_info['database_name']:
        err_message = "Missing 'database_name' parameter."
        err = (err_message, status.HTTP_400_BAD_REQUEST)
        return db_columns, db_details, err
    try:
        engine = create_engine("mysql://{0}:{1}@{2}/{3}".format(
            settings.DATABASES['default']['USER'],
            settings.DATABASES['default']['PASSWORD'],
            settings.DATABASES['default']['HOST'],
            db_info['database_name']
        ))
        with engine.connect() as connection:
            db_info['worksheet_id'] = db_info['worksheet_id'] or db_info['table_name']
            if not db_info['worksheet_id']:
                err_message = "Please provide a table name."
                err = (err_message, status.HTTP_400_BAD_REQUEST)
                return db_columns, db_details, err

            if db_info['worksheet_id'] not in engine.table_names():
                err_message = "Table not found in the provided database."
                err = (err_message, status.HTTP_404_NOT_FOUND)
                return db_columns, db_details, err

            column_list = db_info['select_list']
            for aggregate_type, aggregate_columns in db_info['aggregate'].items():
                column_list.extend('{0}({1}) as {2}_of_{3}'
                                   .format(aggregate_type, aggregate_column, aggregate_type, aggregate_column)
                                   for aggregate_column in aggregate_columns)
            column_list = ['*'] if not column_list else column_list

            if db_info['groupby']:
                if column_list == ['*']:
                    query = 'SELECT * FROM {0} GROUP BY {1}'.format(
                        db_info['worksheet_id'],
                        ','.join(db_info['groupby'])
                    )
                else:
                    query = 'SELECT {0}, {1} FROM {2} GROUP BY {3}'.format(
                        ','.join(column_list),
                        ','.join(db_info['groupby']),
                        db_info['worksheet_id'],
                        ','.join(db_info['groupby'])
                    )
            else:
                query = 'SELECT * FROM {0}'.format(db_info['worksheet_id']) if column_list == ['*'] \
                    else 'SELECT {0} FROM {1}'.format(
                    ','.join(column_list),
                    db_info['worksheet_id']
                )
            query_result = connection.execute(query).fetchall()
            db_details = [row.values() for row in query_result]
            db_columns = query_result[0].keys() if query_result else []
    except:
        err_message = "Something went wrong while getting data from database. Please try again."
        err = (err_message, status.HTTP_500_INTERNAL_SERVER_ERROR)
    return db_columns, db_details, err

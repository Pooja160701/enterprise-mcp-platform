from service import PostgreSQLService

service = PostgreSQLService()


def list_databases():
    return service.list_databases()


def list_tables(schema="public"):
    return service.list_tables(schema)


def describe_table(table):
    return service.describe_table(table)


def table_row_count(table):
    return service.table_row_count(table)


def database_size():
    return service.database_size()


def run_select_query(sql):
    return service.run_select_query(sql)
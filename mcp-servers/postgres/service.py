import os

import psycopg


class PostgreSQLService:
    """
    PostgreSQL helper service.
    All methods return Python dictionaries/lists.
    """

    def __init__(self):

        self.host = os.getenv(
            "POSTGRES_HOST",
            "enterprise-postgres",
        )

        self.port = int(
            os.getenv(
                "POSTGRES_PORT",
                "5432",
            )
        )

        self.database = os.getenv(
            "POSTGRES_DB",
            "enterprise_mcp",
        )

        self.user = os.getenv(
            "POSTGRES_USER",
            "postgres",
        )

        self.password = os.getenv(
            "POSTGRES_PASSWORD",
            "postgres",
        )

    def connection(self):

        return psycopg.connect(
            host=self.host,
            port=self.port,
            dbname=self.database,
            user=self.user,
            password=self.password,
        )

    #
    # ----------------------------
    # DATABASES
    # ----------------------------
    #

    def list_databases(self):

        sql = """
        SELECT datname
        FROM pg_database
        WHERE datistemplate = false
        ORDER BY datname;
        """

        with self.connection() as conn:
            with conn.cursor() as cur:

                cur.execute(sql)

                return [
                    {
                        "name": row[0],
                    }
                    for row in cur.fetchall()
                ]

    #
    # ----------------------------
    # TABLES
    # ----------------------------
    #

    def list_tables(
        self,
        schema: str = "public",
    ):

        sql = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema=%s
        ORDER BY table_name;
        """

        with self.connection() as conn:
            with conn.cursor() as cur:

                cur.execute(
                    sql,
                    (schema,),
                )

                return [
                    {
                        "name": row[0],
                    }
                    for row in cur.fetchall()
                ]

    #
    # ----------------------------
    # DESCRIBE TABLE
    # ----------------------------
    #

    def describe_table(
        self,
        table: str,
    ):

        sql = """
        SELECT
            column_name,
            data_type,
            is_nullable
        FROM information_schema.columns
        WHERE table_name=%s
        ORDER BY ordinal_position;
        """

        with self.connection() as conn:
            with conn.cursor() as cur:

                cur.execute(
                    sql,
                    (table,),
                )

                return [
                    {
                        "column": row[0],
                        "type": row[1],
                        "nullable": row[2],
                    }
                    for row in cur.fetchall()
                ]

    #
    # ----------------------------
    # ROW COUNT
    # ----------------------------
    #

    def table_row_count(
        self,
        table: str,
    ):

        sql = f'SELECT COUNT(*) FROM "{table}"'

        with self.connection() as conn:
            with conn.cursor() as cur:

                cur.execute(sql)

                return {
                    "table": table,
                    "rows": cur.fetchone()[0],
                }

    #
    # ----------------------------
    # DATABASE SIZE
    # ----------------------------
    #

    def database_size(self):

        sql = """
        SELECT
            pg_database_size(current_database()),
            pg_size_pretty(
                pg_database_size(current_database())
            )
        """

        with self.connection() as conn:
            with conn.cursor() as cur:

                cur.execute(sql)

                row = cur.fetchone()

                return {
                    "bytes": row[0],
                    "pretty": row[1],
                }

    #
    # ----------------------------
    # SELECT QUERY
    # ----------------------------
    #

    def run_select_query(
        self,
        sql: str,
    ):

        query = sql.strip().lower()

        if not query.startswith("select"):
            raise ValueError(
                "Only SELECT statements are allowed."
            )

        with self.connection() as conn:

            with conn.cursor() as cur:

                cur.execute(sql)

                columns = [
                    col.name
                    for col in cur.description
                ]

                rows = []

                for record in cur.fetchall():

                    rows.append(
                        dict(
                            zip(
                                columns,
                                record,
                            )
                        )
                    )

                return rows
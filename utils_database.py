class Database:
    """A class to interact with an SQLite database."""

    def __init__(self, conn):
        """Initialize the Database object with a connection object."""
        self.conn = conn

    def get_table_names(self):
        """Retrieve the names of all tables in the database."""
        table_names = []
        query = "SELECT name FROM sqlite_schema WHERE type='table';"
        tables = self.execute(query)
        for table in tables:
            table_names.append(table[0])
        return table_names

    def get_column_names(self, table_name):
        """Retrieve the column names for a given table in the database."""
        column_names = []
        query = f"PRAGMA table_info({table_name});"
        columns = self.execute(query)
        for column in columns:
            column_names.append(column[1])
        return column_names

    def get_database_info(self):
        """Get the structure of the database: table names and their respective columns."""
        database_info = []
        for table_name in self.get_table_names():
            column_names = self.get_column_names(table_name)
            database_info.append(
                {"table_name": table_name, "column_names": column_names}
            )
        return database_info

    def execute(self, query):
        """Execute a provided SQL query and return its results."""
        res = self.conn.execute(query)
        return res.fetchall()

    def close(self):
        """Close the database connection."""
        self.conn.close()

    def get_database_schema(self):
        # Connect to the SQLite database
        # conn = sqlite3.connect(db_path)
        # cursor = conn.cursor()

        # Query the sqlite_master table for table schemas
        tables = self.execute(
            "SELECT name, sql FROM sqlite_master WHERE type='table';")

        # Build the schema representation string
        schema_str = ""

        for table_name, sql in tables:
            # Split the SQL string to extract columns
            lines = sql.split("\n")
            # Exclude the first and last lines
            columns = [line.strip() for line in lines[1:-1]]
            schema_str += f"----------------------------------------\n"
            schema_str += f"Table Name: {table_name}\n"
            schema_str += "Table Columns:\n"

            for column in columns:
                column_parts = column.split(" ", 2)
                field_name = column_parts[0]
                # Joining to handle types like 'INTEGER PRIMARY KEY'
                field_type = " ".join(column_parts[1:]).rstrip(",")
                schema_str += f"   field name: {field_name}, field type: {field_type}\n"

        schema_str += "\n" + "-"*40 + "\n"

        return schema_str

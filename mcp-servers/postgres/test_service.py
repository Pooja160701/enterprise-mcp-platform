from service import PostgreSQLService

db = PostgreSQLService()

print("\nDatabases\n")
print(db.list_databases())

print("\nTables\n")
print(db.list_tables())

print("\nDatabase Size\n")
print(db.database_size())

def __init__(self):

    self.host = "localhost"
    self.port = 5432
    self.database = "enterprise_mcp"
    self.user = "postgres"
    self.password = "postgres"
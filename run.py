from api.models import DatabaseConnection
from api.views import app

if __name__ == '__main__':
    database_connection = DatabaseConnection()

    database_connection.create_tables()
    app.run(debug=True)


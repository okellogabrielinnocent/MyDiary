from api.models import Database
from api.views import app

if __name__ == '__main__':
    database_connection = Database()

    database_connection.create_tables()
    app.run(debug=True)
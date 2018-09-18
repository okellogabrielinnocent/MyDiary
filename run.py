from api.models import Database
from api.views import app

if __name__ == '__main__':
    db_connection = Database()
    db_connection.create_tables()
    app.run(debug=True)
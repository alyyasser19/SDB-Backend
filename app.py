from API import routes
from DataBase import DataBase


app = routes.app
db = DataBase()

if __name__ == '__main__':
    app.run()

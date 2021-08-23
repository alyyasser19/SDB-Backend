from Api import routes
from DataBase import DataBase

# from userRoutes import DataBase

app = routes.app
db = DataBase()

if __name__ == '__main__':
    app.run()

#   To-Do List:
#   
#   sign-in POST - READY DONEEEEEEE
#   change pw POST - READY DONEEEEEEEE  
#   fill ride POST - NOT READY 
#   get ride GET - NOT READY
#   7OTI ASYNC TASKS FEL ROUTING WEL LOCATING! MAINLY EL ROUTING
#   check out the hashing
#   
#

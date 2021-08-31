from Api import routes
import Config

app = routes.app

if __name__ == '__main__':
    app.run(port=5000)

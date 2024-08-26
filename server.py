from flask_app import create_app
from flask_session import Session

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

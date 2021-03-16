from flask import Flask

app = Flask(__name__)

from app.main.routes import main as main_routes
app.register_blueprint(main_routes)

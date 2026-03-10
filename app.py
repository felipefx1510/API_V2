from flask import Flask, render_template, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from config import Config
from models import db
from models.user import User  # noqa: F401
from models.task import Task  # noqa: F401
from routes.user_routes import user_bp
from routes.task_routes import task_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Swagger UI
SWAGGER_URL = "/docs"
API_URL = "/swagger.yaml"

swagger_bp = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)


@app.route("/swagger.yaml")
def swagger_spec():
    return send_from_directory("docs", "swagger.yaml")


@app.route("/")
def index():
    return render_template("index.html")


# Registrar blueprints
app.register_blueprint(user_bp)
app.register_blueprint(task_bp)

# Criar tabelas
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

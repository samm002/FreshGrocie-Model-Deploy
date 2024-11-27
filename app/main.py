from flask import Flask
from .routes import predict_route

app = Flask(__name__)

api_prefix = "/api/v1"

app.register_blueprint(predict_route, url_prefix=f"{api_prefix}")


@app.route(api_prefix)
def index():
    return "Model API is running"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

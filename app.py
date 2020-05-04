from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


# API resources and helpers
from apis.url_shortener import AddLinksHandler, VisitLinksHandler, LinkSearchHandler, LinkStatsHandler


# app initialisation
app = Flask(__name__)
api = Api(app)
db = SQLAlchemy()
app.config[
    'SQLALCHEMY_DATABASE_URI'] = "postgres://nogliaiolltwaf:321112c2eb76b24b7b075d6cf8a9eb9c01f6d93850558418585a6f5598236ec4@ec2-54-165-36-134.compute-1.amazonaws.com:5432/dc17k5gei3dv2a"
db.init_app(app)

# API Routes
api.add_resource(AddLinksHandler, '/v1/addLink/')
api.add_resource(VisitLinksHandler, '/<short_url>')
api.add_resource(LinkSearchHandler, '/v1/search/')
api.add_resource(LinkStatsHandler, '/v1/stats/')


@app.route('/')
def hello():
    return "Health Check"


if __name__ == '__main__':
    app.run()

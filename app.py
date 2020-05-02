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
    'SQLALCHEMY_DATABASE_URI'] = "postgres://eqslhnnfodvtbi:2c84f80f92b9575c53447f0d07dd052124a601aadc730d760e96c5e" \
                                 "764dd9ad8@ec2-34-193-232-231.compute-1.amazonaws.com:5432/d84ki3s7h5slp6"
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

from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource
from helpers.common_helpers import generate_short_link, get_link, search_result, stats_result

db = SQLAlchemy()


class AddLinksHandler(Resource):

    def post(self):
        resp = {"status": 1, "desc": "", "payload": {}}
        params = request.get_json()
        host = request.host_url
        original_url = params.get('original_url')
        return generate_short_link(original_url, resp, host)


class VisitLinksHandler(Resource):

    def get(self, short_url):
        return get_link(short_url)


class LinkSearchHandler(Resource):

    def post(self):
        resp = {"status": 1, "desc": "", "payload": {}}
        params = request.get_json()
        keyword = params.get("keyword")
        return search_result(keyword, resp)


class LinkStatsHandler(Resource):

    def post(self):
        resp = {"status": 1, "desc": "", "payload": {}}
        params = request.get_json()
        short_url = params.get("short_url")
        return stats_result(short_url, resp)
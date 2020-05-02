import string
from random import choices
from dateutil.relativedelta import relativedelta
from flask_restful import abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import datetime as DT
from flask import redirect
db = SQLAlchemy()


def normalised_response(result_object):
    decoded_response = []
    for row in result_object:
        decoded_response.append(dict(row))
    return decoded_response


def update_link_meta(id, visits):
    visits += 1
    query = text(
        "update links set visits=:visits where id=:id")
    db.engine.execute(query, ({'visits': visits, 'id': id}))
    # update series meta
    ts = DT.datetime.now().timestamp()
    meta_query = text(
        "insert into links_meta (link_id, ts) values "
        "(:link_id, :ts)")
    db.engine.execute(meta_query, ({"link_id": id, 'ts': ts}))


def generate_short_link(original_url, resp, host):
    characters = string.digits + string.ascii_letters
    short_url = ''.join(choices(characters, k=4))

    link = normalised_response(db.engine.execute(text(
                "SELECT * FROM links WHERE short_url=:short_url"), ({"short_url": short_url})
            ))
    if link:
        generate_short_link(original_url, resp,  host)
    ts = DT.datetime.now().timestamp()
    query_params = ({
        'original_url': original_url.lower(),
        'short_url': short_url,
        'ts': ts
    })
    query = text(
        "insert into links (original_url, short_url, ts) values "
        "(:original_url, :short_url, :ts)")
    db.engine.execute(query, query_params)
    resp['payload']['original_url'] = original_url
    resp['payload']['short_url'] = host + short_url
    return resp


def get_link(short_url):
    link = normalised_response(db.engine.execute(text(
        "SELECT id, original_url, visits FROM links WHERE short_url=:short_url"), ({"short_url": short_url})
    ))

    if not link:
        abort(404)
    original_link = link[0].get('original_url')
    id = link[0].get('id')
    visits = link[0].get('visits')
    update_link_meta(id, visits)
    return redirect(original_link)


def search_result(keyword, resp):
    keyword = "%" + (keyword).lower() + "%"
    results = normalised_response(db.engine.execute(text(
        "SELECT original_url, short_url, visits as total_visits FROM links WHERE original_url like :keyword"), ({"keyword": keyword})
    ))
    if not results:
        resp['status'] = 0
        resp['desc'] = "No result found"
    resp['payload'] = results
    print(resp)
    return resp


def stats_result(short_url, resp):
    print(short_url)
    results = normalised_response(db.engine.execute(text(
        "SELECT id, original_url, short_url, visits as total_visits FROM links WHERE short_url=:short_url"),
        ({"short_url": short_url})
    ))
    if not results:
        resp['status'] = 0
        resp['desc'] = "Data not found"
        return resp
    current_time = DT.datetime.now()
    print(current_time)
    current_time_one_hour = current_time - relativedelta(hours=1)
    print(current_time_one_hour)
    current_ts = current_time.timestamp()
    current_one_hour_ts = current_time_one_hour.timestamp()
    meta_results = normalised_response(db.engine.execute(text(
        "SELECT count(*) as last_visits FROM links_meta WHERE link_id=:link_id and ts BETWEEN :current_one_hour_ts and :current_ts"),
        ({"link_id": results[0].get("id"), "current_one_hour_ts": str(current_one_hour_ts), "current_ts": str(current_ts)})
    ))
    resp["payload"]["original_url"] = results[0].get("original_url")
    resp["payload"]["short_url"] = results[0].get("short_url")
    resp["payload"]["total_visits"] = results[0].get("total_visits")
    resp["payload"]["last_one_hour_visits"] = meta_results[0].get("last_visits") if meta_results else 0
    return resp

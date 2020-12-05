from flask import Flask, redirect, render_template, request, abort, jsonify

import database as db
import re


app = Flask(__name__)


@app.route('/')
def root():
    return render_template("index.html")


@app.route('/l/<string:dir_hash>')
def hash_dir(dir_hash):
    if not db.hash_assoc_exists(dir_hash):
        return abort(404)
    else:
        return redirect(db.get_hash_assoc(dir_hash), 302)


@app.route('/new', methods=['POST'])
def link():
    json_ = request.get_json(force=True)
    resp = {
        "success": True,
        "err": None,
        "hash": None,
        "link": None
    }
    try:
        if not re.match(re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,'
                                   r'6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'),
                        json_['url']):
            resp['err'] = "Provided link is not a URL"
            raise ValueError()
        insertion = db.insert_link(json_['url'])
        if not insertion:
            raise ValueError()
        resp['hash'] = insertion
        resp['link'] = request.url_root+"l/"+insertion
    except:
        resp['success'] = False
    return jsonify(resp)


if __name__ == '__main__':
    app.run(port=1192)

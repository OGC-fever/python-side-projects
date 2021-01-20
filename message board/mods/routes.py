from flask import json
from flask.json import jsonify
from main import app, db
from .db_crud import post
from flask import render_template, request, redirect, Response, url_for
from io import BytesIO
from .image_process import check_file, make_timg, verify
import sqlite3
import random


@app.route("/<type>/<int:id>", methods=["GET"])
def image_route(id, type):
    data = post.query.filter_by(id=id).first()
    if type == "image":
        image = BytesIO(data.image)
    elif type == "timg":
        image = BytesIO(data.timg)
    else:
        return redirect("msg")
    resp = Response(image, mimetype='image/jpeg', direct_passthrough=True)
    return resp


@app.route("/modal/card", methods=["GET", "POST"])
def card():
    id = request.args.get("id")
    data = post.query.filter_by(id=id).first()
    return render_template("card_modal.html", data=data)


@app.route("/author/<id>", methods=["GET", "POST"])
def author(id):
    data = post.query.filter_by(id=id).first()
    print(id)

    print(data.name)
    return jsonify(data.name)


@app.route("/msg/<id>", methods=["GET", "POST"])
def msg(id):
    data = post.query.filter_by(id=id).first()
    return data.msg


@app.route("/", methods=["GET"])
@app.route("/msg", methods=["GET", "POST"])
def messages():
    code = verify()
    if request.method == "GET":
        data = post.query.order_by(post.id.desc()).all()
        data_count = db.session.query(post.id).count()
        if data_count == 0:
            return render_template("message.html", data="", code=code)
        else:
            return render_template("message.html", data=data, code=code)

    name = request.form['name']
    msg = request.form['msg']
    file = request.files["upload"]
    if name == "":
        name = random.choice(["nobody", "anonymous", "路人甲", "無名"])
    if check_file(file.filename):  # file exist
        image = sqlite3.Binary(make_timg(file, "image").getbuffer())
        timg = sqlite3.Binary(make_timg(file, "timg").getbuffer())
    else:  # file isn't exist
        if msg == "":  # msg isn't exist
            return ("", 204)
        image = None
        timg = None  # msg exist
    data = post(name=name, msg=msg, image=image, timg=timg, code=code)
    data.post()
    return redirect(url_for("messages"))

# @ app.errorhandler(HTTPException)
# @ app.errorhandler(InternalServerError)
# @ app.errorhandler(TypeError)
# def not_found(e):
#     return render_template("oops.html")


if __name__ == "__main__":
    app.run(debug=True)
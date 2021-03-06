from io import BytesIO
from flask import redirect, Response
from mods.db_crud import post
from config import app


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

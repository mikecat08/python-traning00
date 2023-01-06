from flask import Blueprint, render_template

# Blueprintでcrudアプリを生成する
crud = Blueprint(
  "crud",
  __name__,
  template_folder="templetes",
  static_folder="static",
)

# indexエンドポイントを作成しindex.htmlを返す
@crud.route("/")
def index():
  return render_template("crud/index.html")
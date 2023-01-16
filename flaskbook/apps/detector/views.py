from flask import Blueprint, render_template

# templete_folderを指定する（staticは公開しない）
dt = Blueprint("detector", __name__, template_folder="templates")
@dt.route("/")
def index():
  return render_template("detector/index.html")

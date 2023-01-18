# uuidをimportする
import uuid
# Pathをimportする
from pathlib import Path

from apps.app import db
from apps.crud.models import User
from apps.detector.models import UserImage
from flask import (
  Blueprint, 
  render_template, 
  current_app, 
  send_from_directory,
  redirect,
  url_for,
)

# UploadImageFormをimportする
from apps.detector.forms import UploadImageForm

# login_required, current_userをimportする
from flask_login import current_user, login_required


# templete_folderを指定する（staticは公開しない）
dt = Blueprint("detector", __name__, template_folder="templates")

@dt.route("/")
def index():
  # userとUserImageをJoinして画像一覧を取得する
  user_images = (
    db.session.query(User, UserImage)
    .join(UserImage)
    .filter(User.id == UserImage.user_id)
    .all()
  )
  return render_template("detector/index.html", user_images=user_images)

@dt.route("/images/<path:filename>")
def image_file(filename):
  return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)

@dt.route("/upload", methods=["GET", "POST"])
# ログインを必須とする
@login_required
def upload_image():
  # UploadImageFormを利用してバリデーションする
  form = UploadImageForm()
  if form.validate_on_submit():
    # アップロードされた画像ファイルを取得する
    file = form.image.data
    # ファイルのファイル名と拡張子を取得し、ファイル名をuuidに変換する
    ext = Path(file.filename).suffix
    image_uuid_file_name = str(uuid.uuid4()) + ext

    # 画像を保存する
    image_path = Path(
      current_app.config["UPLOAD_FOLDER"], image_uuid_file_name
    )
    file.save(image_path)

    # DBに保存する
    user_image = UserImage(
      user_id=current_user.id, image_path=image_uuid_file_name
    )
    db.session.add(user_image)
    db.session.commit()
  return render_template("detector/upload.html", form=form)
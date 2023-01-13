from apps.app import db
from apps.auth.forms import SignUpForm
from apps.crud.models import User

from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_user

# Blueprintを使ってauthを生成する
auth = Blueprint(
  "auth",
  __name__,
  template_folder="templates",
  static_folder="static"
)

# indexエンドポイントを作成する
@auth.route("/")
def index():
  return render_template("auth/index.html")

# signupエンドポイントを作成する
@auth.route("/signup", methods=["GET", "POST"])
def signup():
  # SignUpFormをインスタンス化する
  form = SignUpForm()
  if form.validate_on_submit():
    user = User(
      username=form.username.data,
      email=form.email.data,
      password=form.password.data,
    )

    # メールアドレスの重複をチェックする
    if user.is_duplicate_email():
      flash("指定のメールアドレスは登録済みです。")
      return redirect(url_for("auth.signup"))

    # ユーザー情報を登録する
    db.session.add(user)
    db.session.commit()
    # ユーザー情報をセッションに格納する
    login_user(user)

    # GETパラメータにnextキーが存在し、値が無い場合はユーザーの一覧ページへリダイレクトする
    next_ = request.args.get("next")
    if next_ is None or not next_.startswith("/"):
      next_ = url_for("crud.users")
    return redirect(next_)

  return render_template("auth/signup.html", form=form)
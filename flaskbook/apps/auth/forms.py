from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignUpForm(FlaskForm):
  username = StringField(
    "ユーザー名",
    validators=[
      DataRequired("ユーザー名は必須です。"),
      Length(1, 30, "30文字以内で入力して下さい。"),
    ],
  )

  email = StringField(
    "メールアドレス",
    validators=[
      DataRequired("メールアドレスは必須です。"),
      Email("メールアドレスの形式で入力して下さい。"),
    ],
  )

  password = PasswordField(
    "パスワード",
    validators=[
      DataRequired("パスワードは必須です。"),
    ],
  )

  submit = SubmitField("新規登録")
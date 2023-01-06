from pathlib import Path
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemyをインスタンス化する
db = SQLAlchemy()

# create_app関数を作成する
def create_app():
  # Flaskインスタンス生成
  app = Flask(__name__)
  # アプリのコンフィグ設定をする
  app.config.from_mapping(
    SECRET_KEY="2AZSMss3p5QPbcY2hBsJ",
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
    SQLALCHEMY_TRACK_MODIFICATIONS=False
  )

  # SQLAlchemyとアプリを連携する
  db.init_app(app)
  # Migrateとアプリを連携する
  Migrate(app, db)

  # crudパッケージからviewsをimportする
  from apps.crud import views as crud_views

  # register_blueprintを使いviewsのcrudをアプリへ登録する
  app.register_blueprint(crud_views.crud, url_prefix="/crud")

  return app
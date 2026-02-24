import os
import sys

ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from flask import Blueprint, render_template, session, url_for, request

from helpers.decorators import authenticated

from database.user_repository import UserRepository
from database.article_repository import ArticleRepository

from forms.article import AddArticleForm

from models.article import Article
from models.user import User

article_bp = Blueprint("articles", __name__, url_prefix="/articles")


@article_bp.route("/add")
@authenticated
def add_article():
    form = AddArticleForm(request.form)
    if request.method == "POST" and form.validate():
        # TODO: add the article in database for the logged user
        pass
    return render_template("article/add_article.html", form=form)


@article_bp.route("/list")
@authenticated
def list_articles():
    # TODO: get all the articles from the database (mine or not) and dislpays them in the list
    articles: list[Article] = []
    return render_template("article/list_article.html", articles=articles)

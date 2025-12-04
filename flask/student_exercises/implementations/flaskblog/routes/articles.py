import sys
import os

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
sys.path.append(ROOT_DIR)

from flask import Blueprint, render_template, request, session, flash, redirect, url_for

from helpers.decorators import authenticated
from forms.article import AddArticleForm
from config.firestore_connection import db, DocumentReference, DocumentSnapshot
from helpers.firestore_funcs import get_user_by_uid
from models.article import Article
from models.user import User

articles_bp = Blueprint("articles", __name__, url_prefix="/articles")


@articles_bp.route("/")
def all_articles() -> str:
    # TODO: display the lats 10 articles
    return ""


@articles_bp.route("/my")
@authenticated
def my_articles() -> str:
    myself_ref: DocumentReference = db.collection("users").document(
        session["firestore_id"]
    )
    my_articles: list[DocumentSnapshot] = (
        db.collection("articles")
        .where("authors", "array_contains", myself_ref)
        .order_by("created_at", direction="DESCENDING")
        .get()
    )
    return render_template(
        "articles/list_articles.html",
        articles=[
            Article.from_dict(article_snapshot.to_dict() | {"id": article_snapshot.id})
            for article_snapshot in my_articles
        ],
    )


@articles_bp.route("/add", methods=["GET", "POST"])
@authenticated
def add_article() -> str:
    form = AddArticleForm(request.form)
    if request.method == "POST" and form.validate():
        # add the article in database
        myself: User = get_user_by_uid(session["uid"], db)
        db.collection("articles").add(
            Article(
                title=form.title.data, body=form.body.data, authors=[myself]
            ).to_dict(include_id=False)
        )
        flash("Article successfully added", "success")
        return redirect(url_for("articles.my_articles"))
    else:
        # display the article add page
        return render_template("articles/add_article.html", form=form)

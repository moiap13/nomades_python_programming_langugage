import os
import sys

ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from flask import Blueprint, flash, redirect, render_template, session, url_for, request

from helpers.decorators import authenticated
from helpers.gemini import GeminiAssistantService

from database.user_repository import UserRepository
from database.article_repository import ArticleRepository

from forms.article import AddArticleForm

from models.article import Article
from models.user import User

article_bp = Blueprint("articles", __name__, url_prefix="/articles")
_article_repository = ArticleRepository()
_user_repository = UserRepository()
article_assistant = GeminiAssistantService(
    "AIzaSyD_HHgwL-1bCkvM4RJcSma7DC7Vwz7i1os",
    "You are a chief redactor for a bloging internet platform",
)


@article_bp.route("/add", methods=["GET", "POST"])
@authenticated
def add_article():
    form = AddArticleForm(request.form, methods=["GET", "POST"])
    if request.method == "POST" and form.validate():
        title: str = form.title.data
        body: str = form.body.data
        body_resumed: str = article_assistant.basic_chat(
            f"Summurize this text in two sentences: {body}"
        )

        authors: list[User] = [
            _user_repository.get_user_by_firestore_id(session["firestore_id"])
        ]
        article = Article("", title, body, authors, body_resumed)
        article_id: str = _article_repository.create_article(article)

        flash(f"Article created with id={article_id}", "success")
        return redirect(url_for("articles.list_my_articles"))
    return render_template("article/add_article.html", form=form)


@article_bp.route("/list")
@authenticated
def list_articles():
    # get all the articles from the database (mine or not) and dislpays them in the list
    articles: list[Article] = _article_repository.get_all()
    current_user = _user_repository.get_user_by_firestore_id(session["firestore_id"])
    return render_template(
        "article/list_article.html",
        articles=articles,
        page_title="All Articles",
        current_user=current_user,
    )


@article_bp.route("/my")
@authenticated
def list_my_articles():
    articles: list[Article] = _article_repository.get_by_user(
        _user_repository.get_user_by_firestore_id(session["firestore_id"])
    )
    current_user = _user_repository.get_user_by_firestore_id(session["firestore_id"])
    return render_template(
        "article/list_article.html",
        articles=articles,
        page_title="My Articles",
        current_user=current_user,
    )


@article_bp.route("/view/<firestore_id>")
@authenticated
def view_articles(firestore_id: str):
    article: Article = _article_repository.get_by_firestore_id(firestore_id)
    current_user: User = _user_repository.get_user_by_firestore_id(
        session["firestore_id"]
    )
    authors_name: list[str] = [user.get_fullname() for user in article.authors]
    return render_template(
        "article/view_article.html",
        article=article,
        page_title="My Articles",
        authors_name=authors_name,
        current_user=current_user,
    )


@article_bp.route("/modify/<firestore_id>", methods=["GET", "POST"])
@authenticated
def modify_article(firestore_id: str):
    form = AddArticleForm(request.form)
    article = _article_repository.get_by_firestore_id(firestore_id)
    current_user = _user_repository.get_user_by_firestore_id(session["firestore_id"])

    if not article.is_user_author(current_user):
        flash("You don't have permission to modify this article", "danger")
        return redirect(url_for("articles.view_articles", firestore_id=article.id))

    if request.method == "POST" and form.validate():
        article.title = form.title.data

        body_resumed = article.body_summury
        if article.body != form.body.data:
            body_resumed: str = article_assistant.basic_chat(
                f"Summurize this text in two sentences: {article.body}"
            )
            article.body = form.body.data
            article.body_summury = body_resumed

        _article_repository.update(article)
        flash(f"Article modified with id={article.id}", "success")
        return redirect(url_for("articles.view_articles", firestore_id=article.id))
    else:
        form.title.data = article.title
        form.body.data = article.body

    return render_template("article/modify_article.html", article=article, form=form)


@article_bp.route("/delete/<firestore_id>", methods=["POST"])
@authenticated
def delete_article(firestore_id: str):
    article = _article_repository.get_by_firestore_id(firestore_id)
    current_user = _user_repository.get_user_by_firestore_id(session["firestore_id"])

    if not article.is_user_author(current_user):
        flash("You don't have permission to delete this article", "danger")
        return redirect(url_for("articles.view_articles", firestore_id=article.id))

    _article_repository.delete_by_firestore_id(firestore_id)
    flash(f"Article deleted with id={firestore_id}", "success")
    return redirect(url_for("articles.list_my_articles"))

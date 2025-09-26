# create the articles blueprint
# the collection name is `articles`
# This blueprint contains 3 routes
# - /articles/all: displays all the articles, the articles come form the database
# - /articles/my: displays all my articles, the articles comes from the database after filtering by the author firestore id
# - /articles/add: add a new article to the database
import os, sys
import json

from flask import Blueprint, render_template, session, request, redirect, url_for, flash

ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
CONFIG_FILE: str = os.path.join(ROOT_DIR, "configs", "config_creds.json")

sys.path.append(ROOT_DIR)

from helpers.decorators import authenticated
from configs.firestore_connector import db, DocumentSnapshot, DocumentReference
from forms.articles import ArticleAddForm
from helpers.google_gemini import GeminiAssistantService

with open(CONFIG_FILE) as json_config:
    config: dict[str, str] = json.load(json_config)

articles_bp = Blueprint("articles", __name__, url_prefix="/articles")

gemini_assistant = GeminiAssistantService(
    api_key=config["gemini_api_key"],
    sys_prompt="You are a blog website reviewer",
    model_name="gemini-2.5-pro",
)


@articles_bp.route("/all")
@authenticated
def articles_show_all():
    all_articles: list[DocumentSnapshot] = db.collection("articles").get()
    articles: list[dict[str, str | dict[str, str | None]]] = []
    for article in all_articles:
        # {
        #     "title": "...",
        #     "body": "...",
        #     "author": DocumentReference(...)
        # }
        article_data: dict[str, str | DocumentReference] = article.to_dict() | {
            "article_id": article.id
        }

        author: DocumentSnapshot = article_data["author"].get()
        if author.exists:
            author_dict_data: dict[str, str] = author.to_dict()
            author_data: dict[str, str] = {
                "firstname": author_dict_data.get("firstname", ""),
                "lastname": author_dict_data.get("lastname", ""),
                "uid": author.id,
            }
        else:
            author_data: dict[str, str | None] = {
                "firstname": "Unknown",
                "lastname": "Author",
                "uid": None,
            }

        articles.append(article_data | {"author": author_data})

    return render_template(
        "articles/list_articles.html",
        articles=articles,
        link_name="articleShowAll",
        list_title="All Articles",
    )


@articles_bp.route("/my")
@authenticated
def articles_show_my():
    user_ref: DocumentReference = db.collection("users").document(session["uid"])
    user_data: dict[str, str] = user_ref.get().to_dict()
    all_articles: list[DocumentSnapshot] = (
        db.collection("articles").where("author", "==", user_ref).get()
    )
    articles: list[dict[str, str | dict[str, str | None]]] = []
    for article in all_articles:
        # {
        #     "title": "...",
        #     "body": "...",
        #     "author": DocumentReference(...)
        # }
        article_data: dict[str, str | DocumentReference] = article.to_dict() | {
            "article_id": article.id
        }

        articles.append(
            article_data
            | {
                "author": {
                    "firstname": user_data.get("firstname", ""),
                    "lastname": user_data.get("lastname", ""),
                    "uid": session.get("uid"),
                }
            }
        )

    return render_template(
        "articles/list_articles.html",
        articles=articles,
        link_name="articleShowMy",
        list_title="My Articles",
    )


@articles_bp.route("/add", methods=["GET", "POST"])
@authenticated
def article_add():
    form = ArticleAddForm(request.form)
    if request.method == "POST" and form.validate():
        title: str = form.title.data
        body: str = form.body.data
        author: DocumentReference = db.collection("users").document(session["uid"])
        gemini_msg: str = gemini_assistant.basic_chat(
            f"summarize this text in a few words: {body}"
        )

        _, added_article = db.collection("articles").add(
            {"title": title, "body": body, "author": author, "gemini_msg": gemini_msg}
        )

        flash(f"Article succesfully added with id {added_article.id}", "success")
        return redirect(url_for("articles.articles_show_my"))

    return render_template(
        "articles/add_article.html", form=form, link_name="articleAdd"
    )


@articles_bp.route("/delete/<article_id>")
@authenticated
def article_delete(article_id: str):
    article_ref: DocumentReference = db.collection("articles").document(article_id)
    author_id: str = article_ref.get().to_dict()["author"].id

    if author_id != session["uid"]:
        flash(
            f"User with id {session['uid']} can not delete article with id {article_id}",
            "danger",
        )
        return redirect(url_for("articles.articles_show_my"))

    article_ref.delete()
    flash(
        "Article successfully deleted",
        "success",
    )
    return redirect(url_for("articles.articles_show_my"))

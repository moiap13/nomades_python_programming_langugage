# Do not forget all these routes should be protected :D
from datetime import datetime

from flask import Blueprint, render_template, request, session, flash, redirect, url_for

post_bp = Blueprint("posts", __name__, url_prefix="/posts")

from forms.posts import PostCreateForm
from config.firestore_connection import db, DocumentReference, DocumentSnapshot
from helpers.decorators import authenticated

# /posts/create, is the route responsible of creating a new post
@post_bp.route("/create", methods=["GET", "POST"])
# Protect the route, this mean I must be logged in to acceed this route
# -> if not loggged in -> redirect(url_for("login.login"))
@authenticated
def create_post():
  
  form = PostCreateForm(request.form)
  if request.method == "POST" and form.validate():
    # TODO: Retrieve the form data
    title: str = form.title.data
    body: str = form.body.data
    #Create a DocumentReference of myself (the logged in user), db.collection("users").document(<USER_DOCUMENT_ID>)
    user_docref: DocumentReference = db.collection("users").document(session["uid"])
    
    # create the post dictionnary to insert it in database
    # The post must contain title: str, body: str, author: DocumentReference
    post_dict: dict[str, str | DocumentReference] = {
      "title": title,
      "body": body,
      "author": user_docref
    }
    # Insert in database the new post in the collection `posts`
    db.collection("posts").add(post_dict)

    # Redirect to /posts/my
    return redirect(url_for("posts.my_posts"))
  return render_template("posts/create_post.html", form=form)

# /posts/my, is the route responsible on listing all my posts (all the posts where the other is myself)
@post_bp.route("/my")
# Protect the route, this mean I must be logged in to acceed this route
# -> if not loggged in -> redirect(url_for("login.login"))
@authenticated
def my_posts():
  # Create a DocumentReference of myself (the logged in user), db.collection("users").document(<USER_DOCUMENT_ID>)
  user_docref: DocumentReference = db.collection("users").document(session["uid"])
  # QUERY: Retrieve all the posts where the author is myself (DocumentReference) where("author", "==", DocumentReference)
  user_posts: list[DocumentSnapshot] = db.collection("posts").where("author", "==", user_docref).get()
  # transform the list of DocumentSnapshot of my posts to a list of dictionnaries
    # Where the author is the firstname and lastname of the DocumentReferebce user
  posts: list[dict[str, str]] = []
  for doc_snapshot in user_posts:
    post_data: dict[str, str | DocumentReference] = doc_snapshot.to_dict()
    user_data: dict[str, str | datetime] = post_data["author"].get().to_dict()
    posts.append({
      "title": post_data["title"],
      "body": post_data["body"],
      "author": f"{user_data['firstname']} {user_data['lastname']}",
      "id": doc_snapshot.id
    })
  
  return render_template("posts/list_posts.html", posts=posts)

# BONUS: Create a route to delete a post
@post_bp.route("/<id>/delete")
@authenticated
def delete_post_by_id(id: str):
  
  post_ref: DocumentReference = db.collection("posts").document(id)
  post_snapshot: DocumentSnapshot = post_ref.get()

  if not post_snapshot.exists:
    flash(f"Post with id {id} doesn't exists", "warning")
    return redirect(url_for("posts.my_posts"))

  author_ref: DocumentReference = post_snapshot.to_dict()["author"]
  user_ref: DocumentReference = db.collection("users").document(session["uid"])

  if user_ref != author_ref:
    flash(f"You tried to delete a post which is not yours", "danger")
    return redirect(url_for("posts.my_posts"))

  post_ref.delete()
  flash("Post successfully deleted", "success")
  return redirect(url_for("posts.my_posts"))

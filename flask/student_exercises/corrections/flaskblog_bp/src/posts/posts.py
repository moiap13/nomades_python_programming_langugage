# Do not forget all these routes should be protected :D

from flask import Blueprint, render_template, request

post_bp = Blueprint("posts", __name__, url_prefix="/posts")

from forms.posts import PostCreateForm
from config.firestore_connection import db

# /posts/create, is the route responsible of creating a new post
@post_bp.route("/create", methods=["GET", "POST"])
def create_post():
  # TODO: Protect the route, this mean I must be logged in to acceed this route
  # -> if not loggged in -> redirect(url_for("login.login"))
  form = PostCreateForm(request.form)
  if request.method == "POST" and form.validate():
    print(form.title.data, form.body.data)
  # TODO: Retrieve the form data and validate them
    # TODO: Create a DocumentReference of myself (the logged in user), db.collection("users").document(<USER_DOCUMENT_ID>)
    # TODO: create the post dictionnary to insert it in database
      # The post must contain title: str, body: str, author: DocumentReference
    # TODO: Insert in database the new post in the collection `posts`
    # TODO: Redirect to /posts/my
  return render_template("posts/create_post.html", form=form)

# /posts/my, is the route responsible on listing all my posts (all the posts where the other is myself)
@post_bp.route("/my")
def my_posts():
  # TODO: Protect the route, this mean I must be logged in to acceed this route
  # -> if not loggged in -> redirect(url_for("login.login"))

  # TODO: Crete a DocumentReference of myself (the logged in user), db.collection("users").document(<USER_DOCUMENT_ID>)
  # TODO: QUERY: Retrieve all the posts where the author is myself (DocumentReference) where("author", "==", DocumentReference)
  # TODO: transform the list of DocumentSnapshot of my posts to a list of dictionnaries
    # Where the author is the firstname and lastname of the DocumentReferebce user
  posts = [
    {
      "title": "Post 1",
      "body": "This is the body of the post 1",
      "author": "John Doe"
    },
    {
      "title": "Post 2",
      "body": "This is the body of the post 2",
      "author": "John Doe"
    },
    {
      "title": "Post 2",
      "body": "This is the body of the post 2",
      "author": "John Doe"
    },
    {
      "title": "Post 2",
      "body": "This is the body of the post 2",
      "author": "John Doe"
    },
    {
      "title": "Post 2",
      "body": "This is the body of the post 2",
      "author": "John Doe"
    },
    {
      "title": "Post 2",
      "body": "This is the body of the post 2 This is the body of the post 2 This is the body of the post 2",
      "author": "John Doe"
    },
  ]
  return render_template("posts/list_posts.html", posts=posts)

# TODO: BONUS: Create a route to delete a post
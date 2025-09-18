import os

from flask import Flask, render_template, request

app = Flask(__name__)

CURR_DIR: str = os.path.dirname(__file__)
UPLOAD_DIR: str = os.path.join(CURR_DIR, "uploads")


@app.route("/first_form", methods=["GET", "POST"])
def first_form() -> str:
    if request.method == "POST":
        firstname: str = request.form["firstname"]
        lastname: str = request.form.get("lastname", "")
        email: str = request.form.get("email", "")

        pp = request.files.get("profile_picture")
        print(pp.content_type)

        if (
            firstname.strip() == ""
            or lastname.strip == ""
            or pp == None
            or (
                pp.content_type.split("/")[-1] != "png"
                and pp.content_type.split("/")[-1] != "jpeg"
            )
        ):
            return "Please fill the form correctly !"

        pp.save(os.path.join(UPLOAD_DIR, pp.filename))
        return f"<h1> Hello {firstname} {lastname} {email}</h1>"
    else:
        return render_template("first_form.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

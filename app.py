from flask import Flask, render_template, abort, request, redirect, url_for, session
import storage
from datetime import date

app = Flask(__name__)

app.secret_key = "dev-secret-change-me"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"


@app.route("/")
def home():
    articles = storage.get_all_articles()
    return render_template("home.html", articles=articles)

@app.route("/article/<int:article_id>")
def show_article(article_id):
    article = storage.get_article(article_id)
    if article is None:
        abort(404)
    return render_template("article.html", article=article)

@app.route("/login", methods = ["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        
        error = "Invalid username or password"

    return render_template("login.html", error = error)


@app.route("/admin")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    articles = storage.get_all_articles()
    return render_template("dashboard.html", articles = articles)



@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("home"))


@app.route("/admin/new", methods =["GET","POST"])
def new_article():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    error = None
    article = {"title": "", "content": "", "date": date.today().isoformat()}
    if request.method == "POST":
        article["title"] = request.form["title"].strip()
        article["content"] = request.form["content"].strip()
        article["date"] = request.form["date"].strip()

        if not article["title"] or not article["content"]:
            error = "Title and content cannot be empty"
        else:
            article["id"] = storage.get_next_id()
            storage.save_article(article)
            return redirect(url_for("dashboard"))

    return render_template("article_form.html", heading="New Article", article=article, error=error)


@app.route("/admin/edit/<int:article_id>", methods=["GET", "POST"])
def edit_article(article_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    article = storage.get_article(article_id)
    if article is None:
        abort(404)

    error = None

    if request.method == "POST":
        article["title"] = request.form["title"].strip()
        article["content"] = request.form["content"].strip()
        article["date"] = request.form["date"]

        if not article["title"] or not article["content"]:
            error = "Title and content cannot be empty"
        else:
            storage.save_article(article)
            return redirect(url_for("dashboard"))

    return render_template("article_form.html", heading="Edit Article", article=article, error=error)


@app.route("/admin/delete/<int:article_id>", methods=["POST"])
def remove_article(article_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    storage.delete_article(article_id)
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
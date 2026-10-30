from flask import Flask, render_template, abort, request, redirect, url_for, session
import storage

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
        redirect(url_for("login"))

    articles = storage.get_all_articles()
    return render_template("dashboard.html", articles = articles)



@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug=True)
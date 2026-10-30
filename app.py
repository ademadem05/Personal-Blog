from flask import Flask, render_template, abort
import storage

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)
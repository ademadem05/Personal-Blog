import json
import os

ARTICLES_DIR = "articles"

def article_path(article_id):
    return os.path.join(ARTICLES_DIR, f"{article_id}.json")

def get_article(article_id):
    path = article_path(article_id)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding= "utf-8") as f:
        return json.load(f)

def get_all_articles():
    os.makedirs(ARTICLES_DIR, exist_ok=True)
    articles = []
    for filename in os.listdir(ARTICLES_DIR):
        if filename.endswith(".json"):
            path = os.path.join(ARTICLES_DIR, filename)
            with open(path,"r", encoding="utf-8") as f:
                articles.append(json.load(f))

    articles.sort(key=lambda article: article["date"], reverse=True)
    return articles

def save_article(article):
    os.makedirs(ARTICLES_DIR, exist_ok=True)
    with open(article_path(article["id"]), "w", encoding="utf-8") as f:
        json.dump(article,f, indent=4, ensure_ascii=False)

def delete_article(article_id):
    path = article_path(article_id)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False


def get_next_id():
    articles = get_all_articles()
    if not articles:
        return 1
    ids = []
    for article in articles:
        ids.append(article["id"])
    return max(ids) + 1


def main():

    save_article({
        "id": get_next_id(),
        "title": "First blog",
        "content": "Hello world this is my first blog text.",
        "date": "2026-10-30",
    })


    for article in get_all_articles():
        print(article["id"], article["date"], article["title"])

    print(get_article(1))
    print(get_article(999))

if __name__ == "__main__":
    main()
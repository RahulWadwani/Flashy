from flask import Flask, render_template,request


import requests

app = Flask(__name__)

NEWS_API_KEY = 'f24643f62bfb4866afb85b939e81e2ad'  # Replace with your NewsAPI key

# We'll store articles globally (better way is to cache properly, but simple for now)
articles_data = []
@app.route('/')
def home():
    query = request.args.get('query')
    category = request.args.get('category')

    if query:
        url = f'https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}'
    elif category:
        url = f'https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={NEWS_API_KEY}'
    else:
        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}'

    response = requests.get(url)
    data = response.json()
    articles = data.get('articles', [])

    # Filter out articles with no image
    articles = [article for article in articles if article.get('urlToImage')]

    return render_template('home.html', articles=articles)

@app.route('/article/<int:article_id>')
def article(article_id):
    global articles_data
    if 0 <= article_id < len(articles_data):
        selected_article = articles_data[article_id]
        return render_template('article.html', article=selected_article)
    else:
        return "Article not found", 404


if __name__ == '__main__':
    app.run(debug=True)
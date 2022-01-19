from Backend.entities.Articles import Articles
from Backend.entities.Categories import Categories
from Backend.entities.Authors import Authors
from flask import Blueprint, request, Response
from app_config import db
from flask import jsonify
import json

articles = Blueprint('articles', __name__)


def json_serial(obj):
    if isinstance(obj, Articles):
        return obj.__dict__
    elif isinstance(obj, Authors):
        return obj.__dict__
    elif isinstance(obj, Categories):
        return obj.__dict__


def getAnswer(text, info=None):
    if info is None:
        info = {}
    res = {
        'status': 'ok',
        'message': text
    }
    answer = {**res, **info}
    return Response(
        response=json.dumps(answer, ensure_ascii=False, default=json_serial),
        mimetype='application/json',
    )
@articles.route('/api/article/get', methods=['GET'])
def api_article_get():
    id = request.values.get('id', 0, int)
    article = Articles.query.filter_by(id=id).first()
    if article is None:
        return jsonify({'status': 'error', 'msg': 'Такой статьи не найдено!'})
    article.views += 1
    db.session.commit()
    return jsonify({'article': article.as_dict()})


@articles.route('/api/articles/count', methods=['GET'])
def api_articles_count():
    return jsonify({'count': Articles.query.count()})


@articles.route('/api/article/popularity', methods=['GET'])
def api_articles_popularity():
    return jsonify({'popularity': Articles.query.order_by(Articles.views.desc()).first().as_dict()})

@articles.route('/api/articles/get')
def api_articles_get():
    page = request.values.get('page', 0, int)
    item_count = 10
    page_offset = 0
    if page > 1:
        page_offset = page * item_count
    articles = Articles.query.order_by(Articles.id.desc()).limit(
        item_count).offset(page_offset).all()
    arts = []
    for art in articles:
        category = art.category.as_dict()
        author = art.author.as_dict()
        article = art.as_dict()
        article['category'] = category
        article['author'] = author
        arts.append(article)
    pages = len(arts) / 10
    if pages < 1:
        pages = 1
    return getAnswer({'page': page, 'articles': arts, 'pages': pages})


@articles.route('/api/article/remove', methods=['DELETE'])
def api_article_remove():
    request_data = request.get_json()
    id = request_data['id']
    print(id)
    article = Articles.query.filter_by(id=id).first()
    if article is None:
        return jsonify({'status': 'error', 'msg': 'Такой статьи не найдено!'})
    db.session.delete(article)
    db.session.commit()
    return jsonify({'status': 'ok', 'msg': 'Статья успешно удалена!'})



@articles.route('/api/article/edit', methods=['PUT'])
def api_article_edit():
    request_data = request.get_json()
    id = request_data['id']
    article = Articles.query.filter_by(id=id).first()
    if article is None:
        return jsonify({'status': 'error', 'msg': 'Такой статьи не найдено!'})
    text = request_data['text'].strip()
    title = request_data['title'].strip()
    category_id = request_data['category_id']
    author_id = request_data['author_id']
    main_img = request_data['main_img'].strip()
    article.text = text
    article.title = title
    article.category_id = category_id
    article.author_id = author_id
    article.main_img = main_img
    db.session.commit()
    return jsonify({'status': 'ok', 'article': article.as_dict()})



@articles.route('/api/article/create', methods=['POST'])
def api_article_create():
    request_data = request.get_json()
    text = request_data['text'].strip()
    title = request_data['title'].strip()
    category_id = request_data['category_id']
    author_id = request_data['author_id']
    main_img = request_data['main_img'].strip()
    article = Articles(text=text, title=title, category_id = category_id, author_id = author_id, main_img = main_img)
    db.session.add(article)
    db.session.commit()
    article = {'id': article.id, 'title': article.title, 'text': article.text, 'main_img': article.main_img}
    return jsonify({'status': 'ok', 'article': article})
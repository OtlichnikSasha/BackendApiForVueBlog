import json
from Backend.entities.Categories import Categories
from flask import Blueprint, request, jsonify, Response
from app_config import db
categories = Blueprint('categories', __name__)


@categories.route('/api/category/get', methods=['GET'])
def api_category_get():
    id = request.values.get('id', 0, int)
    category = Categories.query.filter_by(id=id).first()
    if category is None:
        return jsonify({"msg": "Такой категории не найдено!"}, 400)
    return jsonify(category.as_dict())


@categories.route('/api/category/create', methods=['POST'])
def api_category_create():
    request_data = request.get_json()
    title = request_data['title'].strip()
    text = request_data['text'].strip()
    if title == '' or text == '':
        return jsonify({'msg': 'Не все данные заполнены!'}, 400)
    category = Categories(title=title, text=text)
    db.session.add(category)
    db.session.commit()
    return jsonify(category.as_dict())


@categories.route('/api/category/edit', methods=['PUT'])
def api_category_edit():
    request_data = request.get_json()
    id = request_data['id']
    title = request_data['title'].strip()
    text = request_data['text'].strip()
    category = Categories.query.filter_by(id=id).first()
    if category is None:
        return jsonify({"msg": "Такой категории не найдено!"}, 400)
    if title == '' or text == '':
        return jsonify({'msg': 'Не все данные заполнены!'}, 400)
    category.title = title
    category.text = text
    db.session.commit()
    return jsonify(category.as_dict())

@categories.route('/api/category/remove', methods=['DELETE'])
def api_category_remove():
    request_data = request.get_json()
    id = request_data['id']
    category = Categories.query.filter_by(id=id).first()
    if category is None:
        return jsonify({"msg": "Такой категории не найдено!"}, 400)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'status': 'ok', 'msg': 'Категория успешно удалена!'}, 200)


@categories.route('/api/categories/get', methods=['GET'])
def api_categories_get():
    categories = Categories.query.all()
    cats = []
    for cat in categories:
        cats.append({'id': cat.id, 'title': cat.title, 'text': cat.text})
    return jsonify(cats)


@categories.route('/api/categories/count', methods=['GET'])
def api_categories_count():
    return jsonify({'count': Categories.query.count()})
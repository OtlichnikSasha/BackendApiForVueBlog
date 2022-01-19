from Backend.entities.Authors import Authors
from flask import Blueprint, request, jsonify
from app_config import db
authors = Blueprint('authors', __name__)

@authors.route('/api/authors/get', methods=['GET'])
def api_authors_get():
    authors = Authors.query.all()
    auth = []
    for a in authors:
        auth.append({'id': a.id, 'name': a.name, 'surname': a.surname})
    return jsonify(auth)


@authors.route('/api/authors/count', methods=['GET'])
def api_authors_count():
    return jsonify({'count': Authors.query.count()})

@authors.route('/api/author/create', methods=['POST'])
def api_author_create():
    request_data = request.get_json()
    name = request_data['name'].strip()
    surname = request_data['surname'].strip()
    speciality = request_data['speciality'].strip()
    if name == '' or surname == '' or speciality == '':
        return jsonify({'msg': 'Не все данные заполнены!'}, 400)
    author = Authors(name=name, surname=surname, speciality=speciality)
    db.session.add(author)
    db.session.commit()
    author = {'id': author.id, 'name': author.name, 'surname': author.surname, 'speciality': author.speciality}
    return jsonify({'author': author})



@authors.route('/api/author/remove', methods=['DELETE'])
def api_author_remove():
    request_data = request.get_json()
    id = request_data['id']
    author = Authors.query.filter_by(id=id).first()
    if author is None:
        return jsonify({'msg': 'Не найдено такого автора!'}, 400)
    db.session.delete(author)
    db.session.commit()
    return jsonify({'msg': 'Автор успешно удалён'})
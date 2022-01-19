from app_config import app, db
from Backend.controllers.CategoriesController import categories
from Backend.controllers.ArticlesController import articles
from Backend.controllers.AuthorsController import authors
import flask_cors
from Backend.entities import Articles
from Backend.entities import Categories
from Backend.entities import Authors
app.register_blueprint(authors)
app.register_blueprint(categories)
app.register_blueprint(articles)


# db.create_all()
if __name__ == '__main__':
    app.run()

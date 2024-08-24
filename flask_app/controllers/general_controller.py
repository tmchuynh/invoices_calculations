from flask import Blueprint, render_template, request, redirect, url_for, current_app, jsonify
from flask_app import db
import flask_excel as excel
import re, os

bp = Blueprint('general', __name__)

Session = sessionmaker(bind=engine)

@bp.route("/import", methods=['GET', 'POST'])
def doimport():
    if request.method == 'POST':
        def author_init_func(row):
            c = Author(row['username'])
            c.email = row['email']
            c.id = row['id']
            return c

        def book_init_func(row):
            c = Author.query.filter_by(name=row['author']).first()
            p = Book(row['title'], row['published'], c)
            return p
        request.save_book_to_database(
            field_name='file', session=db.session,
            tables=[Book, Author],
            initializers=[book_init_func, author_init_func])
        return redirect(url_for('.handson_table'), code=302)
    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (xls, xlsx, ods please)</h1>
    <form action="" method=author enctype=multipart/form-data><p>
    <input type=file name=file><input type=submit value=Upload>
    </form>
    '''


@bp.route("/download", methods=['GET'])
def download_file():
    return excel.make_response_from_array([[1, 2], [3, 4]], "csv")

@bp.route("/export", methods=['GET'])
def doexport():
    return excel.make_response_from_tables(db.session, [Author, Book], "xls")

@bp.route("/handson_view", methods=['GET'])
def handson_table():
    return excel.make_response_from_tables(
        db.session, [Author, Book], 'handsontable.html')
    
@bp.route("/custom_export", methods=['GET'])
def docustomexport():
    query_sets = Category.query.filter_by(id=1).all()
    column_names = ['author', 'title']
    return excel.make_response_from_query_sets(query_sets, column_names, "xls")


# insert database related code here
if __name__ == "__main__":
    excel.init_excel(app)
    app.run()
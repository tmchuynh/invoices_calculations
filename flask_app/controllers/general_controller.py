from flask import Blueprint, render_template, request, redirect, url_for, current_app, jsonify
from flask_app import db
import flask_excel as excel
import re, os

bp = Blueprint('general', __name__)

Session = sessionmaker(bind=engine)

@bp.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        return jsonify({"result": request.get_array(field_name='file')})
    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (csv, tsv, csvz, tsvz only)</h1>
    <form action="" method=post enctype=multipart/form-data><p>
    <input type=file name=file><input type=submit value=Upload>
    </form>F
    '''


@bp.route("/download", methods=['GET'])
def download_file():
    return excel.make_response_from_array([[1, 2], [3, 4]], "csv")


@bp.route("/export", methods=['GET'])
def export_records():
    return excel.make_response_from_array([[1, 2], [3, 4]], "csv",
                                          file_name="export_data")


@bp.route("/download_file_named_in_unicode", methods=['GET'])
def download_file_named_in_unicode():
    return excel.make_response_from_array([[1, 2], [3, 4]], "csv",
                                          file_name=u"中文文件名")


# insert database related code here
if __name__ == "__main__":
    excel.init_excel(app)
    app.run()
from flask import Blueprint, jsonify, request, render_template, make_response
from service.tutoria_service import TutoriaService
from repository.repository_impl.tutoria_repo_impl import TutoriaRepoImpl
from sqlalchemy.exc import DataError
from jsonschema.validators import validate
from jsonschema import ValidationError
from validate.jsonschema import json_schema_tutoria
from flask_jwt_extended import jwt_required
from validate.JWT_validate import JWTValidate
from Json.jwt_class import JWT
from flask_weasyprint import HTML, CSS

reports = Blueprint('reports', __name__, url_prefix = "/reports")
tutoria_repository = TutoriaRepoImpl()
tutoria_service = TutoriaService(tutoria_repository)


@reports.route("/reports_tutoria/<string:id_tutoria>", methods = ['GET'])
def reports_tutoria(id_tutoria):
    tutoria = tutoria_service.find_tutoria_by_id(id_tutoria)

    if tutoria:
        rendered = render_template('reporte_tutorias.html', nombre_docente = tutoria['docente']['nombre'], 
        programa = tutoria['docente']['programa'][0]['nombre'], tutoria = tutoria)
        pdf = HTML(string=rendered).write_pdf(stylesheets=[CSS(string='@page { size: A2;')])
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=reporte_tutoria/{tutoria["fecha"]}.pdf'
        return response
    else:
        response_not_found = {
            'status_code' : 404,
            'message' : 'Tutoria no encontrada'
        }
        return jsonify(response_not_found), 404

@reports.route("/reports_tutoria/<string:fecha_inicio>/<string:fecha_final>", methods = ['GET'])
def find_tutoria_between_dates(fecha_inicio, fecha_final):
    tutorias = tutoria_service.find_tutoria_between_dates(fecha_inicio, fecha_final)

    if tutorias:
        rendered = render_template('report_tutoria_masivo.html',tutorias = tutorias)
        pdf = HTML(string=rendered).write_pdf(stylesheets=[CSS(string='@page { size: A2;')])
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=reporte_tutoria.pdf'
        return response
    else:
        response_not_found = {
            'status_code' : 404,
            'message' : 'Tutoria no encontrada'
        }
        return jsonify(response_not_found), 404
    

@reports.route("/reports_tutoria/<string:fecha_inicio>/<string:fecha_final>/<string:documento_docente>", methods = ['GET'])
def find_tutoria_between_dates_docente(fecha_inicio, fecha_final, documento_docente):
    tutorias = tutoria_service.find_tutoria_between_dates_docente(fecha_inicio, fecha_final, documento_docente)

    if tutorias:
        rendered = render_template('report_tutoria_masivo.html',tutorias = tutorias)
        pdf = HTML(string=rendered).write_pdf(stylesheets=[CSS(string='@page { size: A2;')])
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=reporte_tutoria.pdf'
        return response
    else:
        response_not_found = {
            'status_code' : 404,
            'message' : 'Tutoria no encontrada'
        }
        return jsonify(response_not_found), 404
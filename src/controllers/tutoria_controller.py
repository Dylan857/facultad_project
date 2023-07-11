from flask import Blueprint, jsonify, request, render_template, make_response
from service.tutoria_service import TutoriaService
from repository.repository_impl.tutoria_repo_impl import TutoriaRepoImpl
from sqlalchemy.exc import DataError
from jsonschema.validators import validate
from jsonschema import ValidationError
from validate.jsonschema import json_schema_tutoria
from flask_weasyprint import HTML, CSS

tutoria = Blueprint('tutoria', __name__, url_prefix = "/tutoria")
tutoria_repository = TutoriaRepoImpl()
tutoria_service = TutoriaService(tutoria_repository)

@tutoria.route("/create_tutoria", methods = ['POST'])
def create_tutoria():
    
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }
    try:

        data = request.get_json()

        validate(instance=data, schema=json_schema_tutoria)
        
        docente_id = data.get('docente_id')
        fecha = data.get('fecha')
        hora_inicio = data.get('hora_inicio')
        hora_fin = data.get('hora_fin')
        asignatura_id = data.get('asignatura_id')
        estudiantes = data.get('estudiantes')

        new_tutoria = tutoria_service.create_tutoria(docente_id, fecha, hora_inicio, hora_fin, estudiantes, asignatura_id)

        if new_tutoria == True:
            return jsonify(response)
        elif new_tutoria:
            response['status_code'] = 400
            response['message'] = new_tutoria
            return jsonify(response), 400
        
    except DataError as e:
        response['status_code']= 400
        response['message'] = "Proporcione una fecha o hora valida por favor"
        return jsonify(response), 400
    except ValidationError:
        response['status_code'] = 400
        response['message'] = "Hubo un problema al agendar la tutoria"
        return jsonify(response), 400

@tutoria.route("/tutorias")
def get_tutorias():

    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    response['datos'] = tutoria_service.get_tutorias()
    return jsonify(response)

@tutoria.route("/find_tutoria/<string:numero_documento>", methods = ['GET'])
def get_tutoria_by_docente(numero_documento):

    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    tutorias = tutoria_service.find_tutorias_by_docente(numero_documento)
    
    if tutorias == None:
        response['status_code'] = 400
        response['message'] = "Documento de docente no valido"
        return jsonify(response)
    
    elif tutorias:
        response['datos'] = tutorias
        return jsonify(response)
    else:
        response['status_code'] = 404
        response['message'] = "No se encontraron tutorias"
        return jsonify(response)

@tutoria.route("/find_tutoria_fecha/<string:fecha>", methods = ['GET'])
def get_tutoria_by_fecha(fecha):
    
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }
    try:        
        tutorias = tutoria_service.find_tutorias_by_fecha(fecha)

        if tutorias:
            response['datos'] = tutorias
            return jsonify(response)
        else:
            response['status_code'] = 404
            response['message'] = "No se encontraron tutorias"
            return jsonify(response), 404
    except DataError:
        response['status_code'] = 400
        response['message'] = "Proporcione una fecha valida"
        return jsonify(response), 400

@tutoria.route("/find_tutoria_asignatura/<string:asignatura>", methods = ['GET'])
def get_tutoria_by_asignatura(asignatura):

    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }
    tutorias = tutoria_service.find_tutorias_by_asignatura(asignatura)

    if tutorias == None:
        response['status_code'] = 400
        response['message'] = "Asignatura no valida"
        return jsonify(response)
    
    elif tutorias:
        response['datos'] = tutorias
        return jsonify(response)
    
    else:
        response['status_code'] = 404
        response['message'] = "No se encontraron tutorias para esa materia"
    return jsonify(response)

@tutoria.route("/find_tutoria/<string:documento_docente>/<string:fecha>", methods = ['GET'])
def get_tutoria_docente_fecha(documento_docente, fecha):
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    tutorias = tutoria_service.find_tutoria_by_docente_fecha(documento_docente, fecha)
    if tutorias:
        response['datos'] = tutorias
        return jsonify(response)
    else:
        response['status_code'] = 404
        response['message'] = "No se encontraron tutorias"
        return jsonify(response)

@tutoria.route("find_tutoria/<string:fecha>/<string:asignatura>", methods = ['GET'])
def get_tutoria_fecha_asignatura(fecha, asignatura):
    
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }
    tutorias = tutoria_service.find_tutoria_by_fecha_asignatura(fecha, asignatura)

    if tutorias:
        response['datos'] = tutorias
        return jsonify(response)
    else:
        response['status_code'] = 404
        response['message'] = "No se econtraron tutorias"
        return jsonify(response)
    
@tutoria.route("/find_tutoria/<string:documento_docente>/<string:asignatura>", methods = ['GET'])
def get_tutoria_docente_asignatura(documento_docente, asignatura):

    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    tutorias = tutoria_service.find_tutoria_by_docente_asignatura(documento_docente, asignatura)
    if tutorias:
        response['datos'] = tutorias
        return jsonify(response)
    else:
        response['status_code'] = 404
        response['message'] = "No se encontraron tutorias"
        return jsonify(response)

@tutoria.route("/find_tutoria/<string:documento_docente>/<string:fecha>/<string:asignatura>", methods = ['GET'])
def get_tutoria_docente_fecha_asignatura(documento_docente, fecha, asignatura):
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    tutorias = tutoria_service.find_tutoria_by_docente_fecha_asignatura(documento_docente, fecha, asignatura)
    if tutorias:
        response['datos'] = tutorias
        return jsonify(response)
    else:
        response['status_code'] = 404
        response['message'] = "No se encontraron tutorias"
        return jsonify(response)

@tutoria.route("/get_tutorias_soon/<string:documento_docente>", methods = ['GET'])
def get_tutorias_soon(documento_docente):
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    tutorias = tutoria_service.get_tutorias_soon(documento_docente)

    if tutorias:
        response['datos'] = tutorias
        return jsonify(response)
    else:
        response['status_code'] = 404
        response['message'] = "No tiene tutorias pendientes"
        return jsonify(response)
    

@tutoria.route("/get_tutorias_soon_admin", methods = ['GET'])
def get_tutorias_soon_admin():
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    tutorias = tutoria_service.get_tutorias_soon_admin()

    if tutorias:
        response['datos'] = tutorias
        return jsonify(response)
    else:
        response['status_code'] = 404
        response['message'] = "No tiene tutorias pendientes"
        return jsonify(response)
    
@tutoria.route("/count_tutorias_month_by_docente/<string:documento_docente>", methods = ['GET'])
def count_tutorias_month_by_docente(documento_docente):
    
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'count' : 0
    }

    count_tutorias = tutoria_service.count_tutorias_month_by_docente(documento_docente)
    if count_tutorias:
        response['count'] = count_tutorias
        return jsonify(response)
    else:
        response['count'] = 0
        return jsonify(response)

@tutoria.route("/count_tutorias_month_admin", methods = ['GET'])
def count_tutorias_month_admin():
    
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'count' : 0
    }

    count_tutorias = tutoria_service.count_tutorias_month_admin()
    if count_tutorias:
        response['count'] = count_tutorias
        return jsonify(response)
    else:
        response['count'] = 0
        return jsonify(response)


@tutoria.route("/count_tutorias_week_by_docente/<string:documento_docente>", methods = ['GET'])
def count_tutorias_week_by_docente(documento_docente):
    
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'count' : 0
    }

    count_tutorias = tutoria_service.count_tutorias_week_by_docente(documento_docente)
    if count_tutorias:
        response['count'] = count_tutorias
        return jsonify(response)
    else:
        response['count'] = 0
        return jsonify(response)
    
@tutoria.route("/count_tutorias_week_admin", methods = ['GET'])
def count_tutorias_week_admin():
    
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'count' : 0
    }

    count_tutorias = tutoria_service.count_tutorias_week_admin()
    if count_tutorias:
        response['count'] = count_tutorias
        return jsonify(response)
    else:
        response['count'] = 0
        return jsonify(response)
    
@tutoria.route("/count_tutorias_day_by_docente/<string:documento_docente>", methods = ['GET'])
def count_tutorias_day_by_docente(documento_docente):
    
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'count' : 0
    }

    count_tutorias = tutoria_service.count_tutorias_day_by_docente(documento_docente)
    if count_tutorias:
        response['count'] = count_tutorias
        return jsonify(response)
    else:
        response['count'] = 0
        return jsonify(response)
    
@tutoria.route("/count_tutorias_day_admin", methods = ['GET'])
def count_tutorias_day_admin():
    
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'count' : 0
    }

    count_tutorias = tutoria_service.count_tutorias_day_admin()
    if count_tutorias:
        response['count'] = count_tutorias
        return jsonify(response)
    else:
        response['count'] = 0
        return jsonify(response)

@tutoria.route("/update_tutoria/<string:id>", methods = ['PUT'])
def update_tutoria(id):

    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }
    try:

        data = request.get_json()
        
        docente_id = data.get('docente_id')
        fecha = data.get('fecha')
        hora_inicio = data.get('hora_inicio')
        hora_fin = data.get('hora_fin')
        asignatura_id = data.get('asignatura_id')
        estudiantes = data.get('estudiantes')

        tutoria_edit = tutoria_service.update_tutoria(id, docente_id, fecha, hora_inicio, hora_fin, estudiantes, asignatura_id)

        if tutoria_edit == True:
            return jsonify(response)
        elif tutoria_edit:
            response['status_code'] = 400
            response['message'] = tutoria_edit
            return jsonify(response), 400
        else:
            response['status_code'] = 404
            response['message'] = 'Tutoria no encontrada'
            return jsonify(response), 404
    except DataError as e:
        response['status_code']= 400
        response['message'] = "Proporcione una fecha o hora valida por favor"
        return jsonify(response), 400
    
@tutoria.route("/delete_tutoria/<string:id>", methods = ['DELETE'])
def delete_tutoria(id):

    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    delete_tutoria = tutoria_service.delete_tutoria(id)

    if delete_tutoria:
        return jsonify(response)
    else:
        response['status_code'] = 404
        response['message'] = "Tutoria no encontrada"
        return jsonify(response)
    

@tutoria.route("/reports_tutoria")
def reports_tutoria():
    # datos_reporte = obtener_datos_reporte()
    rendered = render_template('reporte_tutorias.html', nombre_docente = "Evelio Arrieta", programa = "Ingeniera Telematica")
    pdf = HTML(string=rendered).write_pdf(stylesheets=[CSS(string='@page { size: A4; margin: 1cm }')])
    response = make_response(pdf)

    # Crea una respuesta del tipo application/pdf
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte.pdf'

    return response

def obtener_datos_reporte():
    return {
        'titulo': 'Reporte de ejemplo',
        'descripcion': 'Este es un reporte de ejemplo generado con Flask y WeasyPrint',
        'datos': [1, 2, 3, 4, 5]
    }
json_schema = {
    "type" : "object",
    "properties" : {
        "nombre" : {"type" : "string", "maxLength" : 50, "pattern": "^(?!\\s*$).+"},
        "celular" : {"type" : "string", "pattern": "^[0-9]+$"},
        "email" : {"type" : "string", "maxLength" : 50, "format" : "email"},
        "tipo_identificacion" : {"type" : "string", "maxLength" : 5, "pattern": "^(?!\\s*$).+"},
        "numero_identificacion" : {"type" : "string", "pattern": "^[0-9]+$", "maxLength" : 15},
        "password" : {"type" : "string", "maxLength" : 255},
        "roles" : {
            "type" : "array",
            "items" : {"type" : "string"},
            "minItems" : 1
        }
    },
    "required" : ["nombre", "celular", "email", "tipo_identificacion", "numero_identificacion", "password", "roles"]
}

json_schema_solicitud = {
    "type" : "object",
    "properties" : {
        "cedula_estudiante" : {"type" : "string", "pattern": "^[0-9]+$", "maxLength" : 15},
        "cedula_docente" : {"type" : "string", "pattern": "^[0-9]+$", "maxLength" : 15},
        "descripcion_solicitud" : {"type" : "string", "maxLength" : 255, "pattern": "^(?!\\s*$).+"}
    },

    "required" : ["cedula_estudiante", "cedula_docente", "descripcion_solicitud"]
}

json_schema_tutoria = {
    "type" : "object",
    "properties" : {
        "docente_id" : {"type" : "string", "maxLength" : 50},
        "fecha" : {"type" : "string"},
        "hora_inicio" : {"type" : "string"},
        "hora_fin" : {"type" : "string"},
        "asignatura_id" : {"type" : "string", "maxLength" : 50},
        "estudiantes" : {"type" : "array",
            "items" : {"type" : "string"},
            "minItems" : 1
            }
    },

    "required" : ["docente_id", "fecha", "hora_inicio", "hora_fin", "asignatura_id", "estudiantes"]
}
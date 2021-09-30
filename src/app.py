from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util # decorar el formato json que viene en binario
from bson.objectid import ObjectId # hacer busquedas por ObjectId
import json

app = Flask(__name__)

app.secret_key = "misecret123aa"

# Conexión a la bd MongoDB
app.config['MONGO_URI'] = 'mongodb://localhost:56702/bdcliente'
mongo = PyMongo(app) # conexion de la aplicación con MongoDB

# EndPoint - rutas para el CRUD

@app.route('/cliente', methods=['POST'])
def create_cliente():
    ccnit = request.json['ccnit']
    nombre = request.json['nombre']
    telefono = request.json['telefono']
    direccion = request.json['direccion']
    estado = request.json['estado']

    if ccnit and nombre and telefono and direccion and estado:
        id = mongo.db.cliente.insert(
            {'ccnit':ccnit,'nombre':nombre, 'telefono':telefono, 'direccion':direccion, 'estado':estado}
        )
        response = jsonify({
            '_id':str(id),
            'ccnit':ccnit,
            'nombre':nombre,
            'telefono':telefono,
            'direccion':direccion,
            'estado':estado
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/cliente',methods=['GET'])
def get_clientes():
    cliente = mongo.db.cliente.find()
    response = json_util.dumps(cliente)
    return Response(response, mimetype = 'application/json')


@app.route('/cliente/<id>', methods=['GET'])
def get_cliente(id):
    print(id)
    cliente = mongo.db.cliente.find_one({'_id':ObjectId(id)})
    response = json_util.dumps(cliente)
    return Response(response, mimetype = 'application/json')


@app.route('/cliente/<id>', methods = ['DELETE'])
def delete_cliente(id):
    mongo.db.cliente.delete_one({'_id':ObjectId(id)})
    response = jsonify({'message':'Product '+id+' deleted successfully'})
    response.status_code = 200
    return response


@app.route('/cliente/<_id>', methods=['PUT'])
def update_cliente(_id):
    ccnit = request.json['ccnit']
    nombre = request.json['nombre']
    telefono = request.json['telefono']
    direccion = request.json['direccion']
    estado = request.json['estado']

    if ccnit and nombre and telefono and direccion and estado and _id:
        mongo.db.cliente.update_one(
            {'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
            {'$set':{'ccnit':ccnit,'nombre':nombre, 'telefono':telefono, 'direccion':direccion, 'estado':estado}}
        )
        response = jsonify({'message':'Product '+_id+' update successfully'})
        response.status_code = 200
        return response
    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message':'Resource not found '+request.url,
        'status':404
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True,port=3600)
    
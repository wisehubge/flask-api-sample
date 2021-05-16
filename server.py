from flask import Flask, jsonify, request
import json
app = Flask(__name__)


def read_services():
    with open('services.json', 'r') as data:
        services = json.load(data)
    return services


def write_services(services):
    with open("services.json", 'w') as data:
        json.dump(services, data, indent=4)


@app.route("/services", methods=["GET"])
def all_services():
    services = read_services()
    return jsonify(services)


@app.route("/services", methods=["POST"])
def create_service():
    new_service = request.json
    services = read_services()
    for service in services:
        if service["id"] == new_service["id"]:
            return jsonify("Service ID already exists"), 400
    services.append(new_service)
    write_services(services)
    return jsonify(new_service)


@app.route("/services/<int:id>", methods=["GET"])
def get_service(id):
    services = read_services()
    for service in services:
        if service["id"] == id:
            return jsonify(service)
    return jsonify(f"Service with ID: {id} not found"), 404


@app.route("/services/<int:id>", methods=["PUT"])
def update_service(id):
    services = read_services()
    update_service = request.json
    for service in services:
        if service["id"] == id:
            if not "active" in update_service and not "name" in update_service and not "complexity" in update_service and not "description" in update_service:
                return jsonify("Nothing to update"), 400
            if "active" in update_service:
                service["active"] = update_service["active"]
            if "name" in update_service:
                service["name"] = update_service["name"]
            if "complexity" in update_service:
                service["complexity"] = update_service["complexity"]
            if "description" in update_service:
                service["description"] = update_service["description"]
            write_services(services)
            return jsonify(service)
    return jsonify(f"Service with ID: {id} not found"), 404


@app.route("/services/<int:id>", methods=["DELETE"])
def delete_service(id):
    services = read_services()
    for service in services:
        if service["id"] == id:
            services.remove(service)
            write_services(services)
            return jsonify(service)
    return jsonify("Service not found"), 404

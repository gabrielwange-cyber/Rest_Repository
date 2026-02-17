from flask import Flask, jsonify, render_template, Blueprint, request
import json
import os


# http://127.0.0.1:5000 
# http://127.0.0.1:5000/get/list
# http://127.0.0.1:5000/add/car
# http://127.0.0.1:5000/update/car
# http://127.0.0.1:5000/remove/car

cars_bp = Blueprint("cars_bp", __name__)

# http://127.0.0.1:5000 
@cars_bp.route("/", methods=["GET"])
def home():
    return render_template("home.html")
 
# http://127.0.0.1:5000/get/list 
@cars_bp.route("/get/list", methods=["GET"])
def get_cars():
    with open("Cars.json", "r") as f:
        cars = json.load(f)
    return jsonify(cars)


@cars_bp.route("/add/", methods=["POST"])
def add_car():
    with open("Cars.json", "r") as f_regnr_check:
        cars_data = json.load(f_regnr_check)
    new_car = {
        "make": request.json["make"].upper(),
        "model": request.json["model"].upper(),
        "year": request.json["year"],
        "regnr": request.json["regnr"].upper()
    }
    
    Regnr = new_car["regnr"].upper()
    if Regnr in cars_data:
        return jsonify({
            "error": "Car with this registration number already exists."
        }), 400
    
    else:
        cars_data[Regnr] = new_car
        with open("Cars.json", "w") as f_add_car:
            json.dump(cars_data, f_add_car, indent=4) 
        return jsonify(new_car), 200

@cars_bp.route("/update/", methods=["PUT"])
def update_car():
    with open("Cars.json", "r") as f_update_car:
        update_cars_data = json.load(f_update_car)
    
    user_data = request.get_json()
    
    regnr_to_update = user_data.get("regnr")
    regnr_to_update = regnr_to_update.upper()

    if regnr_to_update not in update_cars_data:
        return jsonify({"error": "Car with this registration number does not exist."}), 404
    
    else:
        update_cars_data[regnr_to_update] = {
            "make": user_data["make"].upper(),
            "model": user_data["model"].upper(),
            "year": user_data["year"],
            "regnr": regnr_to_update
        }
        
        with open("Cars.json", "w") as f_update_car:
            json.dump(update_cars_data, f_update_car, indent=4)
        return jsonify({"message": "Car updated successfully"}), 200

@cars_bp.route("/remove/", methods=["DELETE"])
def remove_car():
    with open("Cars.json", "r") as f_remove_car:
        remove_cars_data = json.load(f_remove_car)
    
    user_data = request.get_json()
    user_data_regnr = user_data.get("regnr").upper()
    
    if user_data_regnr not in remove_cars_data:
        return jsonify({"error": "Car with this registration number does not exist."}), 404
    
    else:
        del remove_cars_data[user_data_regnr]
        
        with open("Cars.json", "w") as f_remove_car:
            json.dump(remove_cars_data, f_remove_car, indent=4)
        return jsonify({"message": "Car removed successfully"}), 200
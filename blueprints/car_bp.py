from flask import Flask, jsonify, render_template, Blueprint, request
import json
import os


# http://127.0.0.1:5000 
# http://127.0.0.1:5000/get/list
# http://127.0.0.1:5000/add/car
# http://127.0.0.1:5000/update/car
# http://127.0.0.1:5000/remove/car

cars_bp = Blueprint("cars_bp", __name__)

"""  http://127.0.0.1:5000 
@cars_bp.route("/", methods=["GET"])
def home():
    return render_template("home.html") """



################################### shows all cars in the json file ###################################
@cars_bp.route("/", methods=["GET"])
def get_cars():
    return jsonify(load_cars())

##################################### shows a specific car based on the registration number ###################################
@cars_bp.route("/get/car/<regnr>", methods=["GET"])
def get_car_by_regnr(regnr):
    cars = load_cars()
    regnr = regnr.upper() 

    if regnr.upper() in cars:
        return jsonify(cars[regnr.upper()])
    else:
        return jsonify({"error": "Car not found"}), 404

################################### adds a new car to the json file ###################################
@cars_bp.route("/add/", methods=["POST"])
def add_car():
    cars_data = load_cars()
    data = request.get_json() #takes the data from the user and saves it in a new dictionary
    

    new_car = {  # We choose to make all of the elements upper to avoid issues with input
        "make": data["make"].upper(),
        "model": data["model"].upper(),
        "year": data["year"],
        "regnr": data["regnr"].upper()
    }
    
    Regnr = new_car["regnr"].upper()
    if Regnr in cars_data:
        return jsonify({
            "error": "Car with this registration number already exists."
        }), 400
    
    else:
        cars_data[Regnr] = new_car
        save_cars(cars_data)
        return jsonify(new_car), 200
    
################################### updates a car in the json file ###################################
@cars_bp.route("/update/", methods=["PUT"])
def update_car():
    cars = load_cars()
    data = request.get_json()

    regnr = data["regnr"].upper()

    if regnr not in cars:
        return jsonify({"error": "Car with this registration number does not exist."}), 404
    
    else:
        cars[regnr] = {
        "make": data["make"].upper(),
        "model": data["model"].upper(),
        "year": data["year"],
        "regnr": regnr
        }
        
        save_cars(cars)
        return jsonify({"message": "Car updated successfully"}), 200


################################### removes a car from the json file ###################################
@cars_bp.route("/remove/", methods=["DELETE"])
def remove_car():
    cars = load_cars()
    user_data = request.get_json() 
    user_data_regnr = user_data.get("regnr").upper()
    
    if user_data_regnr not in cars:
        return jsonify({"error": "Car with this registration number does not exist."}), 404
    
    else:
        del cars[user_data_regnr] #Del removes the car with the specified registration number from the dictionary
        
        save_cars(cars)
        return jsonify({"message": "Car removed successfully"}), 200
    

###################################### functions to load and save cars from the json file ###################################
def  load_cars():
    try:
        with open("cars.json", "r") as f:
            cars = json.load(f)
            return cars
    except FileNotFoundError:
        return {}
    
def save_cars(cars):
    with open("Cars.json", "w") as f:
        json.dump(cars, f, indent=4)
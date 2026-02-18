from flask import Flask, jsonify, Blueprint, render_template, request
import json
import os


from blueprints.car_bp import cars_bp


app = Flask(__name__)
app.register_blueprint(cars_bp)


if __name__ == "__main__":
    app.run(debug=True)
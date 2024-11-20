from flask import Blueprint, jsonify, request
from utils import extract_text
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return jsonify({"message": "hello mic check 1, 2, 3"})

@main.route("/extract_text", methods=["POST"])
def get_text_from_file():
   data = request.json()
   file_name  = data["file_name"]
   text  = extract_text(file_name)
   return jsonify({"text": text}),200

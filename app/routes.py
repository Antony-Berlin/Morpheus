from flask import Blueprint, jsonify, request

from .utils import extract_text,get_topics
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return jsonify({"message": "hello mic check 1, 2, 3"})

@main.route("/extract_text", methods=["POST"])
def get_text_from_file():
   data = request.json
   file_name  = data["file_name"]
   text  = extract_text(file_name)
   return jsonify({"text": text}),200

@main.route("/get_topics", methods=["POST"])
def get_topics_from_text():
    data = request.json
    text = data["text"]
    topics = get_topics(text)
    return jsonify({"topics": topics}),200

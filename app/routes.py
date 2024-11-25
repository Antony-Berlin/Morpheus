from flask import Blueprint, jsonify, request

from .utils import extract_text, get_topics, get_questions_and_answers, handle_file_upload
import os
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return jsonify({"message": "hello mic check 1, 2, 3"})


@main.route("/upload_file", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    response, status_code = handle_file_upload(file)
    return jsonify(response), status_code

@main.route("/get_files", methods=["GET"])
def get_files():
    print("getting files...")
    files = os.listdir("Documents")
    print(files)
    return jsonify({"files": files}), 200

@main.route("/delete_file", methods=["POST"])
def delete_file():
    data = request.json
    file_name = data["file_name"]
    if not os.path.exists(f"Documents/{file_name}"):
        return jsonify({"error": "File does not exist"}), 404
    os.remove(f"Documents/{file_name}")
    return jsonify({"message": "file deleted"}), 204
        
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

@main.route("/get_questions", methods=["POST"])
def get_questions_from_topic():
    data = request.json
    topic = data["topic"]
    about_prof = data["about_prof"]
    prof_sample_question = data["prof_sample_question"]
    file_text = data["file_text"]
    no_of_quesitons = data["no_of_questions"]
    questions,status_code = get_questions_and_answers(topic, file_text, about_prof, prof_sample_question, no_of_quesitons)
    return jsonify(questions),status_code

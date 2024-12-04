from flask import Blueprint, jsonify, request

from .utils import extract_text, get_topics, get_questions_and_answers, handle_file_upload, add_proff_profile, get_proff_profile_data, delete_proff_profile_data, get_all_proff_name
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
    no_of_questions = data["no_of_questions"]
    topics = get_topics(text, no_of_questions)
    return jsonify({"topics": topics}),200

@main.route("/get_questions", methods=["POST"])
def get_questions_from_topic():
    data = request.json
    topic = data["topic"]
    about_prof = data["about_prof"]
    prof_sample_question = data["prof_sample_question"]
    file_text = data["file_text"]
    no_of_quesitons = data["no_of_questions"]
    prev_questions = data["questions"]
    questions,status_code = get_questions_and_answers(topic, file_text, about_prof, prof_sample_question, no_of_quesitons, prev_questions)
    return jsonify(questions),status_code

@main.route("/add_proff_profile", methods=["POST"])
def add_proff():
    data = request.json
    prof_name = data["prof_name"]
    about_prof = data["about_prof"]
    prof_sample_question = data["prof_sample_question"]
    response, status_code = add_proff_profile(prof_name, about_prof, prof_sample_question)
    return jsonify(response), status_code

@main.route("/get_proff_profile", methods=["POST"])
def get_proff_profile():
    proff_name = request.json["proff_name"]
    response, status_code = get_proff_profile_data(proff_name)
    return jsonify(response), status_code

@main.route("/delete_proff_profile", methods=["POST"])
def delete_proff_profile():
    data = request.json
    prof_name = data["proff_name"]
    response, status_code = delete_proff_profile_data(prof_name)
    return jsonify(response), status_code

@main.route("/get_all_proff_profile", methods=["GET"])
def get_all_proff():
    response, status_code = get_all_proff_name()
    return jsonify(response), status_code


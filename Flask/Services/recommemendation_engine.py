from flask import request, jsonify
from Utils.cosine_similarity import calculate_cosine_similarity
import json
import os

# Safely load questions data
question_file_path = os.path.join(os.path.dirname(__file__), '../QuestionSet.json')
with open(question_file_path, "r") as f:
    questions_data = json.load(f)

def recommend_questions():
    if request.method == "GET":
        return jsonify({"message": "Please use POST to recommend questions."}), 405

    try:
        user_data = request.get_json(force=True)
    except Exception as e:
        return jsonify({"error": f"Invalid JSON payload: {str(e)}"}), 400

    user_expertise = user_data.get("expertise", [])
    user_level = user_data.get("level")

    # Validate input
    if not user_expertise or not isinstance(user_expertise, list):
        return jsonify({"error": "Invalid or missing 'expertise'. Expected a list."}), 400
    if not user_level:
        return jsonify({"error": "Missing 'level' field."}), 400

    # Filter questions by level
    filtered_questions = [q for q in questions_data if q.get("level") == user_level]

    if not filtered_questions:
        return jsonify({"error": f"No questions found for level '{user_level}'."}), 404

    # Calculate cosine similarity scores
    scored_questions = []
    for question in filtered_questions:
        question_keywords = question.get("keywords", [])
        similarity_score = calculate_cosine_similarity(user_expertise, question_keywords)
        scored_questions.append((question["id"], question["question"], similarity_score))

    # Sort and take top 5
    top_questions = sorted(scored_questions, key=lambda x: x[2], reverse=True)[:5]

    # Build response list
    top_questions_dict_list = [
        {"question_id": q[0], "question_text": q[1], "score": q[2]}
        for q in top_questions
    ]

    return jsonify({"recommended_questions": top_questions_dict_list}), 200

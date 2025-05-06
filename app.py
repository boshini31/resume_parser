import time
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

from utils.resume_parser import extract_text_from_resume
from utils.skill_extractor import extract_skills

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Load the cleaned Coursera course dataset
try:
    course_df = pd.read_csv("courses.csv")
except Exception as e:
    print(f"Error loading courses.csv: {e}")
    course_df = pd.DataFrame(columns=["course_title", "course_time", "course_skills"])

@app.route('/recommend', methods=['POST'])
def recommend_courses():
    start_time = time.time()

    if 'resume' not in request.files:
        return jsonify({"error": "Resume file not provided"}), 400

    resume_file = request.files['resume']
    resume_text = extract_text_from_resume(resume_file)
    candidate_name, skills = extract_skills(resume_text)

    if not skills:
        print(f"Request time: {time.time() - start_time:.2f}s")
        return jsonify({
            "employee_name": candidate_name,
            "matched_courses": []
        }), 200

    matched_courses = []
    for _, row in course_df.iterrows():
        course_skills = str(row.get("course_skills", "")).lower()
        if any(skill.lower() in course_skills for skill in skills):
            matched_courses.append({
                "course_title": row.get('course_title', 'Unknown'),
                "course_duration": row.get('course_time', 'N/A')
            })

    print(f"Request time: {time.time() - start_time:.2f}s")

    return jsonify({
        "employee_name": candidate_name,
        "matched_courses": matched_courses
    })

if __name__ == '__main__':
    app.run(debug=True)

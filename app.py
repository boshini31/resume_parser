import time
import requests
from flask import Flask, request, jsonify
import pandas as pd
from utils.resume_parser import extract_text_from_resume
from utils.skill_extractor import extract_skills

app = Flask(__name__)

SPRING_BOOT_API_URL = 'http://localhost:8085/api/course-mapping/recommend'  # Change to your Spring Boot API URL

@app.route('/recommend', methods=['POST'])
def recommend_courses():
    start_time = time.time()  # Start measuring time

    if 'resume' not in request.files:
        return jsonify({"error": "Resume file not provided"}), 400

    resume_file = request.files['resume']
    resume_text = extract_text_from_resume(resume_file)
    candidate_name, skills = extract_skills(resume_text)

    if not skills:
        end_time = time.time()  # End measuring time
        print(f"Request processing time: {end_time - start_time} seconds")
        return jsonify({
            "employee_name": candidate_name,
            "matched_courses": []
        }), 200

    # Send skills to Spring Boot API for course recommendation
    response = send_skills_to_springboot(skills)

    end_time = time.time()  # End measuring time
    print(f"Request processing time: {end_time - start_time} seconds")

    if response.status_code == 200:
        matched_courses = response.json()
        return jsonify({
            "employee_name": candidate_name,
            "matched_courses": matched_courses
        })
    else:
        return jsonify({"error": "Error fetching course recommendations from Spring Boot API"}), 500

def send_skills_to_springboot(skills):
    # Send a POST request to the Spring Boot API with the extracted skills
    payload = {
        "skills": skills
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(SPRING_BOOT_API_URL, json=payload, headers=headers)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

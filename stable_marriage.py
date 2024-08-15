import csv
import os
import pandas as pd
import numpy as np
from numpy.linalg import norm

# read startup data into array or np array
with open('data/startup_data.csv','r', encoding='utf-8') as f:
    reader = csv.reader(f)
    startup_data = [row for row in reader][1:]

startup_names = [row[0] for row in startup_data]

# startup_profile is a matrix consisting of float numbers that represents the companies preference for each skill
startup_profile = np.array([row[1:] for row in startup_data], dtype=float)

# Read student data from CSV
with open('data/student_data.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    student_data = [row for row in reader][1:]
    
student_names = [row[0] for row in student_data]
student_profiles = np.array([row[1:] for row in student_data], dtype=float)


result = {}
for i in range(len(student_names)):
    startup = startup_profile[i]
    # We have 74 similarity results for each dot product, representing the start matching score to every student
    cos_sim = np.dot(student_profiles, startup) / (norm(startup_profile) * norm(student_profiles))

    # Rank the students by cosine similarity, output is indices
    cos_sim_ranking = np.argsort(cos_sim)[::-1][:10]
    ranking = [(student_names[j], cos_sim[j]) for j in cos_sim_ranking]
    result[startup_names[i]] = ranking

# Sample Data Generation
skills = ['Python', 'Marketing', 'Product Management']
skill_scale = range(0, 8)  # 0-7

# Generate companies with preferred skills
companies = {}
for i in range(150):
    company_name = f'Company_{i+1}'
    preferred_skills = {skill: random.choice(skill_scale) for skill in skills}
    companies[company_name] = preferred_skills

# Generate students with their skills
students = {}
for i in range(150):
    student_name = f'Student_{i+1}'
    student_skills = {skill: random.choice(skill_scale) for skill in skills}
    students[student_name] = student_skills

# Function to calculate preference score
def calculate_score(preferred_skills, candidate_skills):
    score = 0
    for skill in skills:
        # Difference between company's preference and student's skill
        score -= abs(preferred_skills[skill] - candidate_skills[skill])
    return score

# Generate preference lists
company_prefs = {}
for company, pref_skills in companies.items():
    preferences = []
    for student, stu_skills in students.items():
        score = calculate_score(pref_skills, stu_skills)
        preferences.append((score, student))
    # Sort students based on scores (higher score = better)
    preferences.sort(reverse=True)
    company_prefs[company] = [student for score, student in preferences]

student_prefs = {}
for student, stu_skills in students.items():
    preferences = []
    for company, pref_skills in companies.items():
        score = calculate_score(pref_skills, stu_skills)
        preferences.append((score, company))
    preferences.sort(reverse=True)
    student_prefs[student] = [company for score, company in preferences]

# Stable Marriage Algorithm
free_students = list(students.keys())
engagements = {}

# Keep track of proposals
proposals = {student: [] for student in students}

while free_students:
    student = free_students.pop(0)
    student_pref_list = student_prefs[student]
    
    for company in student_pref_list:
        if company in proposals[student]:
            continue  # Already proposed
        proposals[student].append(company)
        
        if company not in engagements:
            engagements[company] = student
            break
        else:
            current_student = engagements[company]
            company_pref_list = company_prefs[company]
            if company_pref_list.index(student) < company_pref_list.index(current_student):
                engagements[company] = student
                free_students.append(current_student)
                break
    else:
        # If student has proposed to all companies and none accepted, assign None
        engagements[f'No Match for {student}'] = student

# Display the matchings
for company, student in engagements.items():
    if 'No Match' in company:
        print(f"{student} was not matched with any company.")
    else:
        print(f"{company} is matched with {student}.")

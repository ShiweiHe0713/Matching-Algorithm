import csv
import random
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
startup_profiles = np.array([row[1:] for row in startup_data], dtype=float)
# startup_profiles[:, 0:8] = startup_profiles[:, 0:8] / 7

# Read student data from CSV
with open('data/student_data.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    student_data = [row for row in reader][1:]

student_names = [row[0] for row in student_data]
student_profiles = np.array([row[1:] for row in student_data], dtype=float)

startup_preferences = {}
student_preferences = {}
for i, startup in enumerate(startup_profiles):
    cos_sim = np.dot(student_profiles, startup) / (norm(startup_profiles) * norm(student_profiles))

    # Rank the students by cosine similarity, output is indices
    cos_sim_ranking = np.argsort(cos_sim)[::-1]
    startup_ranking = [(student_names[j]) for j in cos_sim_ranking]
    startup_preferences[startup_names[i]] = startup_ranking

# Preference list for student_preferences
for i, student in enumerate(student_profiles):
    cos_sim = np.dot(startup_profiles, student) / (norm(student_profiles) * norm(startup_profiles))
    cos_sim_ranking = np.argsort(cos_sim)[::-1]
    student_ranking = [(startup_names[j]) for j in cos_sim_ranking]
    student_preferences[student_names[i]] = student_ranking

def stable_marriage(student_prefs, company_prefs):
    # Initialize all companies and students as free
    free_students = list(student_prefs.keys())
    matches = {}
    proposals = {student: [] for student in student_prefs}  # To track who the students have proposed to

    # Initialize all companies' current engagements as None
    company_engaged = {company: None for company in company_prefs}

    while free_students:
        student = free_students.pop(0)  # Get the first free student
        
        # Get the student's preference list
        student_pref_list = student_prefs[student]

        # Loop through the student's preference list and propose
        for company in student_pref_list:
            if company not in proposals[student]:
                proposals[student].append(company)  # Mark that the student has proposed to this company
                
                # If the company is free, engage the student with the company
                if company_engaged[company] is None:
                    company_engaged[company] = student
                    matches[student] = company
                    break
                
                # If the company is already engaged, check preferences
                else:
                    current_student = company_engaged[company]
                    company_pref_list = company_prefs[company]

                    # If the company prefers the current student over the new student
                    if company_pref_list.index(current_student) < company_pref_list.index(student):
                        # Company stays with current student, continue
                        continue
                    else:
                        # The company prefers the new student, so the current student becomes free
                        free_students.append(current_student)
                        company_engaged[company] = student
                        matches[student] = company
                        break
    
    return matches

matches = stable_marriage(student_preferences, startup_preferences)
print(matches)
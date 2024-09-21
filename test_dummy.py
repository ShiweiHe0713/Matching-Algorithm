import csv
import random
import os
import pandas as pd
import numpy as np
from numpy.linalg import norm

# read startup data into array or np array
with open('data/startup_data_dummy.csv','r', encoding='utf-8') as f:
    reader = csv.reader(f)
    startup_data = [row for row in reader][1:]

startup_names = [row[0] for row in startup_data]
# startup_profile is a matrix consisting of float numbers that represents the companies preference for each skill
startup_profiles = np.array([row[1:] for row in startup_data], dtype=float)

# Read student data from CSV
with open('data/student_data_dummy.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    student_data = [row for row in reader][1:]
    
student_names = [row[0] for row in student_data]
student_profiles = np.array([row[1:] for row in student_data], dtype=float)

# Printing startup and its profile
# for startup, data in zip(startup_names, startup_profiles):
#     print(startup, data)

result = {}
# the normal case is the number of student is smaller than number of startups
# which means students are guaranteed to have a match
n = min(len(student_names), len(startup_names))
for i in range(n):
    startup = startup_profiles[i]
    # We have 74 similarity results for each dot product, representing the start matching score to every student
    # 4 * 13 dot 13 * 1 => 4 * 1
    cos_sim = np.dot(student_profiles, startup) / (norm(startup_profiles) * norm(student_profiles))

#     # Rank the students by cosine similarity, output is indices
    cos_sim_ranking = np.argsort(cos_sim)[::-1][:10]
    ranking = [(student_names[j], cos_sim[j]) for j in cos_sim_ranking]
    result[startup_names[i]] = ranking


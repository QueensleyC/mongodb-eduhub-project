# eduhub_queries.py
# MongoDB operations using PyMongo for the EduHub project

from pymongo import MongoClient, ASCENDING
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from faker import Faker
import random
import string
import time


fake = Faker()
# ========== Part 1: Database Setup and Data Modeling ==========

# Task 1.1: Create Database and Collections
client = MongoClient("mongodb://localhost:27017/")
db = client["eduhub_db"]

# Task 1.2: Design Document Schemas
# (Handled by schema validation in MongoDB setup)

# ========== Part 2: Data Population ==========

# Task 2.1: Insert Sample Data

# Generate 25 users with a mix of roles (students and instructors)
users = []
for i in range(25):
    role = random.choice(["student", "instructor"])
    users.append({
        "userId": f"u{i+1:03}",
        "email": fake.unique.email(),
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "role": role,
        "dateJoined": fake.date_time_between(start_date='-2y', end_date='now'),
        "profile": {
            "bio": fake.sentence(),
            "avatar": fake.image_url(),
            "skills": random.sample(["Python", "JavaScript", "MongoDB", "SQL", "Data Science", "Machine Learning"], k=random.randint(1, 4))
        },
        "isActive": True
    })

db.users.insert_many(users)


# Generate 8 courses, each assigned to a random instructor from users
instructors = [u for u in users if u["role"] == "instructor"]

categories = ["Programming", "Data Science", "Design", "Database", "Cybersecurity"]
levels = ["beginner", "intermediate", "advanced"]

courses = []
for i in range(8):
    instructor = random.choice(instructors)
    courses.append({
        "courseId": f"c{i+1:03}",
        "title": fake.sentence(nb_words=4),
        "description": fake.paragraph(),
        "instructorId": instructor["userId"],
        "category": random.choice(categories),
        "level": random.choice(levels),
        "duration": round(random.uniform(5, 40), 1),
        "price": round(random.uniform(10, 100), 2),
        "tags": random.sample(["Python", "MongoDB", "Cloud", "UX", "Networks"], k=2),
        "createdAt": datetime.now(),
        "updatedAt": datetime.now(),
        "isPublished": random.choice([True, False])
    })

db.courses.insert_many(courses)


# Generate 15 enrollments linking students to courses with progress info
students = [u for u in users if u["role"] == "student"]

enrollments = []
for i in range(15):
    student = random.choice(students)
    course = random.choice(courses)
    enrollments.append({
        "enrollmentId": f"e{i+1:03}",
        "studentId": student["userId"],
        "courseId": course["courseId"],
        "enrolledAt": fake.date_time_between(start_date='-1y', end_date='now'),
        "progress": round(random.uniform(0, 100), 2),
        "completed": random.choice([True, False])
    })

db.enrollments.insert_many(enrollments)


# Generate 25 lessons assigned randomly to courses
lessons = []
for i in range(25):
    course = random.choice(courses)
    lessons.append({
        "lessonId": f"l{i+1:03}",
        "courseId": course["courseId"],
        "title": fake.sentence(nb_words=5),
        "content": fake.paragraph(nb_sentences=3),
        "videoUrl": fake.url(),
        "duration": round(random.uniform(5, 30), 2),  # duration in minutes
        "order": random.randint(1, 10)
    })

db.lessons.insert_many(lessons)


# Generate 10 assignments linked to random courses with due dates
assignments = []
for i in range(10):
    course = random.choice(courses)
    assignments.append({
        "assignmentId": f"a{i+1:03}",
        "courseId": course["courseId"],
        "title": fake.sentence(),
        "description": fake.paragraph(),
        "dueDate": datetime.now() + timedelta(days=random.randint(5, 20))
    })

db.assignments.insert_many(assignments)


# Generate 12 assignment submissions by students with grades
submissions = []
for i in range(12):
    assignment = random.choice(assignments)
    student = random.choice(students)
    submissions.append({
        "submissionId": f"s{i+1:03}",
        "assignmentId": assignment["assignmentId"],
        "studentId": student["userId"],
        "submittedAt": datetime.now() - timedelta(days=random.randint(0, 10)),
        "content": fake.text(),
        "grade": round(random.uniform(0, 100), 2)
    })

db.submissions.insert_many(submissions)




# Task 2.2: Data Relationships
# (Assured during data insertion using reference fields)

# ========== Part 3: Basic CRUD Operations ==========

# Task 3.1: Create Operations

def add_student_user(user):
    return db.users.insert_one(user)

def create_course(course):
    return db.courses.insert_one(course)

def enroll_student(enrollment):
    return db.enrollments.insert_one(enrollment)

def add_lesson_to_course(lesson):
    return db.lessons.insert_one(lesson)

# Task 3.2: Read Operations

def get_active_students():
    return list(db.users.find({"role": "student", "isActive": True}))

def get_course_with_instructor(course_id):
    return db.courses.aggregate([
        {"$match": {"courseId": course_id}},
        {"$lookup": {
            "from": "users",
            "localField": "instructorId",
            "foreignField": "userId",
            "as": "instructor"
        }}
    ])

def get_courses_by_category(category):
    return list(db.courses.find({"category": category}))

def get_students_in_course(course_id):
    return db.enrollments.aggregate([
        {"$match": {"courseId": course_id}},
        {"$lookup": {
            "from": "users",
            "localField": "studentId",
            "foreignField": "userId",
            "as": "student"
        }}
    ])

def search_courses_by_title(title_fragment):
    return list(db.courses.find({"title": {"$regex": title_fragment, "$options": "i"}}))

# Task 3.3: Update Operations

def update_user_profile(user_id, update_fields):
    return db.users.update_one({"userId": user_id}, {"$set": update_fields})

def mark_course_published(course_id):
    return db.courses.update_one({"courseId": course_id}, {"$set": {"isPublished": True}})

def update_assignment_grade(submission_id, grade):
    return db.assignment_submissions.update_one({"_id": ObjectId(submission_id)}, {"$set": {"grade": grade}})

def add_tags_to_course(course_id, tags):
    return db.courses.update_one({"courseId": course_id}, {"$addToSet": {"tags": {"$each": tags}}})

# Task 3.4: Delete Operations

def soft_delete_user(user_id):
    return db.users.update_one({"userId": user_id}, {"$set": {"isActive": False}})

def delete_enrollment(enrollment_id):
    return db.enrollments.delete_one({"_id": ObjectId(enrollment_id)})

def remove_lesson(lesson_id):
    return db.lessons.delete_one({"_id": ObjectId(lesson_id)})

# ========== Part 4: Advanced Queries and Aggregation ==========

# Task 4.1: Complex Queries

def find_courses_in_price_range():
    return list(db.courses.find({"price": {"$gte": 50, "$lte": 200}}))

def recent_users():
    six_months_ago = datetime.now() - timedelta(days=180)
    return list(db.users.find({"dateJoined": {"$gte": six_months_ago}}))

def find_courses_with_tags(tags):
    return list(db.courses.find({"tags": {"$in": tags}}))

def assignments_due_next_week():
    now = datetime.now()
    next_week = now + timedelta(days=7)
    return list(db.assignments.find({"dueDate": {"$gte": now, "$lte": next_week}}))

# Task 4.2: Aggregation Pipeline

# Count total enrollments per course
db.enrollments.aggregate([
    {"$group": {"_id": "$courseId", "totalEnrollments": {"$sum": 1}}}
])

# Calculate average course rating
db.courses.aggregate([
    {"$match": {"rating": {"$exists": True}}},
    {"$group": {"_id": "$courseId", "avgRating": {"$avg": "$rating"}}}
])

# Group by course category
db.courses.aggregate([
    {"$group": {"_id": "$category", "totalCourses": {"$sum": 1}}}
])

# Average grade per student
db.submissions.aggregate([
    {"$group": {"_id": "$studentId", "averageGrade": {"$avg": "$grade"}}}
])

# Completion rate by course
db.enrollments.aggregate([
    {"$group": {
        "_id": "$courseId",
        "avgProgress": {"$avg": "$progress"}  # Assuming progress is from 0 to 100
    }}
])

# Top-performing students (e.g., avg grade ≥ 90)
db.submissions.aggregate([
    {"$group": {"_id": "$studentId", "averageGrade": {"$avg": "$grade"}}},
    {"$match": {"averageGrade": {"$gte": 90}}},
    {"$sort": {"averageGrade": -1}}
])

# Total students taught by each instructor
db.courses.aggregate([
    {"$lookup": {
        "from": "enrollments",
        "localField": "courseId",
        "foreignField": "courseId",
        "as": "course_enrollments"
    }},
    {"$group": {
        "_id": "$instructorId",
        "totalStudents": {"$sum": {"$size": "$course_enrollments"}}
    }}
])

# Average course rating per instructor
db.courses.aggregate([
    {"$match": {"rating": {"$exists": True}}},
    {"$group": {
        "_id": "$instructorId",
        "averageRating": {"$avg": "$rating"}
    }}
])

# Revenue generated per instructor
db.courses.aggregate([
    {"$lookup": {
        "from": "enrollments",
        "localField": "courseId",
        "foreignField": "courseId",
        "as": "enrolls"
    }},
    {"$project": {
        "instructorId": 1,
        "revenue": {"$multiply": [{"$size": "$enrolls"}, "$price"]}
    }},
    {"$group": {
        "_id": "$instructorId",
        "totalRevenue": {"$sum": "$revenue"}
    }}
])

# Monthly enrollment trends
db.enrollments.aggregate([
    {"$group": {
        "_id": {"$dateToString": {"format": "%Y-%m", "date": "$enrollmentDate"}},
        "totalEnrollments": {"$sum": 1}
    }},
    {"$sort": {"_id": 1}}
])

# Most popular course categories
db.enrollments.aggregate([
    {"$lookup": {
        "from": "courses",
        "localField": "courseId",
        "foreignField": "courseId",
        "as": "course"
    }},
    {"$unwind": "$course"},
    {"$group": {"_id": "$course.category", "total": {"$sum": 1}}},
    {"$sort": {"total": -1}}
])

# Student engagement metrics (average progress per course)
db.enrollments.aggregate([
    {"$group": {
        "_id": "$courseId",
        "avgProgress": {"$avg": "$progress"}
    }}
])


# ========== Part 5: Indexing and Performance ==========

# Task 5.1: Index Creation

def create_indexes():
    db.users.create_index("email", unique=True)
    db.courses.create_index([("title", ASCENDING), ("category", ASCENDING)])
    db.assignments.create_index("dueDate")
    db.enrollments.create_index([("studentId", ASCENDING), ("courseId", ASCENDING)])

# Task 5.2: Query Optimization

def explain_and_time(query_func):
    start = time.time()
    explanation = query_func().explain()
    end = time.time()
    print("Execution Time: {:.4f} seconds".format(end - start))
    return explanation

# ========== Part 6: Data Validation and Error Handling ==========

# Task 6.1: Schema Validation
# (Handled in MongoDB collection options or programmatically)

# Task 6.2: Error Handling

def insert_with_error_handling(collection, document):
    try:
        collection.insert_one(document)
    except Exception as e:
        print(f"Insertion failed: {e}")

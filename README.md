# EduHub MongoDB Project

A MongoDB-powered backend prototype for an educational platform called **EduHub**, built using PyMongo and Python 3.10.9 with MongoDB version 8.0.8. This project covers a wide range of database operations including schema validation, indexing, advanced queries, and performance optimization.

---

## 📁 Project Structure

```
├── eduhub_queries.py     # Python code containing all MongoDB operations
├── validation.json       # JSON schema validation rules for collections
├── README.md             # Project documentation
```

---

## 🚀 Setup Instructions

1. **Install MongoDB** and ensure it's running locally on `mongodb://localhost:27017/`.
2. **Install dependencies**:
   ```bash
   pip install pymongo faker pandas
   ```
3. **Run the script**:
   ```bash
   python eduhub_queries.py
   ```
4. Optional: Use **MongoDB Compass** to visually inspect data.

---

## 🗃️ Database Schema Documentation

### users
```json
{
  "userId": "string (unique)",
  "email": "string (required, unique)",
  "firstName": "string",
  "lastName": "string",
  "role": "string (student/instructor)",
  "dateJoined": "datetime",
  "profile": {
    "bio": "string",
    "avatar": "string",
    "skills": ["string"]
  },
  "isActive": true
}
```

### courses
```json
{
  "courseId": "string (unique)",
  "title": "string (required)",
  "description": "string",
  "instructorId": "string (userId)",
  "category": "string",
  "level": "string (beginner/intermediate/advanced)",
  "duration": "float (hours)",
  "price": "float",
  "tags": ["string"],
  "createdAt": "datetime",
  "updatedAt": "datetime",
  "isPublished": true
}
```

### enrollments
```json
{
  "enrollmentId": "string (unique)",
  "studentId": "string (userId)",
  "courseId": "string (courseId)",
  "enrollmentDate": "datetime",
  "progress": "float (0.0 - 1.0)",
  "isComplete": "boolean"
}
```

### lessons
```json
{
  "lessonId": "string (unique)",
  "courseId": "string (courseId)",
  "title": "string",
  "content": "string",
  "videoUrl": "string",
  "duration": "float",
  "createdAt": "datetime"
}
```

### assignments
```json
{
  "assignmentId": "string (unique)",
  "courseId": "string",
  "title": "string",
  "description": "string",
  "dueDate": "datetime"
}
```

### submissions
```json
{
  "submissionId": "string (unique)",
  "assignmentId": "string",
  "studentId": "string",
  "submittedAt": "datetime",
  "grade": "float"
}
```

---

## 🔎 Query Explanations

### Basic Operations

- **Create**: Add users, courses, lessons, and enrollments.
- **Read**: Retrieve students, filter by category, fetch course + instructor info.
- **Update**: Profile updates, grades, publishing status.
- **Delete**: Soft deletes (users), remove lessons/enrollments.

### Complex Queries

- Courses priced between $50 and $200.
- Users joined in last 6 months using `$gte` + `datetime.now()`.
- Tag-based searches using `$in`.
- Due dates with `$lt` for upcoming assignments.

### Aggregation Pipelines

- **Course Enrollment Stats**: `$group` by course, count enrollments.
- **Student Performance**: `$group` by studentId, average grades.
- **Instructor Analytics**: `$group` by instructorId, revenue, rating.
- **Advanced Analytics**: Monthly trends using `$month`, popular categories using `$sortByCount`.

---

## ⚡ Performance Analysis

### Before Indexing (Query: search course by title)

```python
start = time.time()
db.courses.find({"title": {"$regex": "python", "$options": "i"}}).explain()
end = time.time()
print("Time before index:", end - start)
```

Time taken: **~0.04s**

### After Indexing

```python
db.courses.create_index([("title", 1)])
start = time.time()
db.courses.find({"title": {"$regex": "python", "$options": "i"}}).explain()
end = time.time()
print("Time after index:", end - start)
```

Time taken: **~0.005s**

### Other Indexed Fields

- `email` on `users` collection
- `dueDate` on `assignments`
- Compound index on `enrollments` for `studentId` and `courseId`

---

## ⚠️ Challenges Faced

### 1. **Schema Enforcement in MongoDB**
   - Solution: Used `validation.json` and MongoDB Compass validator.

### 2. **Handling Complex Aggregations**
   - Grouping by course and instructor required careful `$lookup` and `$unwind` usage.

### 3. **Query Optimization**
   - Used `explain()` and `create_index()` to dramatically improve performance.

### 4. **Error Handling**
   - Duplicate key errors handled with `try-except`.
   - Type errors checked before insertion using Python type guards.

---

## ✅ Outcome

This project demonstrates strong skills in:
- MongoDB modeling
- PyMongo CRUD + Aggregations
- Schema validation and indexing
- Real-world data design for EdTech

---

## 🔗 Author

**Your Name**  
_Developer, Data Enthusiast_  
Email: youremail@example.com  
GitHub: [github.com/yourusername](https://github.com/yourusername)


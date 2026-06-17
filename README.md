# 📚 Library Management REST API

A RESTful Library Management System built with FastAPI that manages books, students, and book issue/return transactions.

The project demonstrates backend development concepts such as CRUD operations, data validation, computed fields, business logic, inventory management, and date-based calculations.

---

## 🚀 Features

### 👨‍🎓 Student Management

* Add Student
* Update Student Information
* Delete Student
* Get Student by ID
* Student Label Generation

### 📚 Book Management

* Add Books
* Update Book Details
* Delete Books
* Get Book by ID
* Automatic Availability Status
* Book Label Generation

### 🔄 Issue & Return Management

* Issue Books to Students
* Return Books
* Automatic Book Inventory Update
* Due Date Tracking
* Overdue Detection
* Borrow Duration Calculation
* Late Fee Calculation

---

## 🛠 Technologies Used

* Python
* FastAPI
* Pydantic V2
* JSON Storage
* REST API
* DateTime Handling

---

## 📂 Project Structure

```text
.
├── main.py
├── books.json
├── student.json
├── Issue.json
└── README.md
```

---

## 📚 Book Model

```json
{
  "Book_id": "SF076",
  "Title": "Nameless Monster",
  "Author": "Franz Bonaparta",
  "Category": "Picture Book",
  "Total_copies": 100
}
```

### Computed Fields

* book_label
* is_available

---

## 👨‍🎓 Student Model

```json
{
  "Student_ID": "SU148",
  "Name": "Jay",
  "Class": 12
}
```

### Computed Fields

* student_label

---

## 🔄 Issue Transaction Model

```json
{
  "Transaction_id": "T001",
  "Student_ID": "SU148",
  "Book_ID": "SF076",
  "issuedate": "2026-06-17",
  "Due_date": "2026-06-24",
  "returndate": null
}
```

### Automatic Calculations

✅ Transaction Status

✅ Is Overdue

✅ Overdue Days

✅ Late Fee

✅ Borrow Duration

✅ Remaining Days

---

## 📌 API Endpoints

### Home

```http
GET /
```

---

### Student APIs

```http
GET    /student_data
GET    /load_student_data/{student_id}
POST   /create_student_data
PUT    /update_student_data/{student_id}
DELETE /delete/{student_id}
```

---

### Book APIs

```http
GET    /books_data
GET    /load_books_data/{book_id}
POST   /create_book_data
PUT    /update_book/{book_id}
DELETE /delete_book/{book_id}
```

---

### Transaction APIs

```http
GET    /issue_data
GET    /issue/{Transaction_id}
POST   /create_issue_data
PUT    /update_Transaction/{Transaction_id}
DELETE /delete_Transaction/{Transaction_id}
```

---

## ⚡ Business Logic

This project automatically:

* Decreases book quantity when a book is issued.
* Increases book quantity when a book is returned.
* Calculates overdue days.
* Calculates late fees.
* Tracks borrowing duration.
* Checks book availability before issuing.

---

## ▶️ Run Locally

Install dependencies:

```bash
pip install fastapi uvicorn pydantic
```

Run server:

```bash
uvicorn main:app --reload
```

---

## 📖 API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## 🎯 Concepts Demonstrated

* REST API Development
* FastAPI Framework
* Pydantic Models
* CRUD Operations
* Computed Fields
* Inventory Management
* Business Logic
* Date Calculations
* JSON Persistence
* Backend Development

---

## 🔮 Future Improvements

* SQLite/PostgreSQL Integration
* JWT Authentication
* Docker Support
* Pagination
* Search Books by Title
* Fine Payment Gateway
* Unit Testing
* Cloud Deployment

---

## 👨‍💻 Author

**Jay Valsur**

Python Developer | FastAPI Enthusiast | Backend Development Learner

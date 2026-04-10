# 📚 BookBridge – Backend API

BookBridge is a peer-to-peer book sharing platform where users can lend, borrow, and manage books within a local virtual library ecosystem.
This backend is built using **Django** and **Django REST Framework (DRF)**, providing a robust API for handling complex workflows such as borrowing, requests, extensions, penalties, and premium memberships.

---

##  Features

### 👤 Authentication & Users

* JWT-based authentication (login, register, logout)
* Profile management (bio, image, contact info)
* Soft delete & account deactivation
* User rating & review system

---

### 📚 Book Management

* Create and manage books
* Categorization & tagging
* Search, filter, and ordering support
* Cover image upload support

---

### 📦 Book Copies

* Multiple copies per book
* Ownership tracking
* Availability status (available / borrowed / unavailable)
* Condition tracking (new / good / old)

---

### 🔁 Borrowing System

* Borrow request system (user → owner)
* Owner approval/rejection flow
* Automatic BorrowRecord creation on acceptance
* Controlled Request limits-based on existing active records and overdue records
* Full lifecycle:

  ```
  Request → Accept → Borrow → Return
  ```

---

### ⏳ Borrow Records

* Tracks borrower, owner, and book copy
* Due date management
* Return tracking
* Overdue detection (dynamic, no cron jobs)
* Extension count tracking

---

### 🔄 Extension System

* Borrowers can request extensions
* Owners can accept/reject extension requests
* Extension history maintained per record
* Controlled extension limits

---

### 💰 Late Fine System

* Automatic overdue detection
* Fine calculation based on delay duration
* Integrated with payment system (planned/)
* Restricts borrowing for overdue users

---

### 💎 Premium Membership

* Subscription-based membership system
* Benefits include:

  * Higher borrow limits
  * Longer borrowing duration
  * Reduced late fines
  * Priority in request queue
* Membership lifecycle (active, expired)

---

### ⭐ Review System

* Book reviews (rating + feedback)
* User reviews (peer-to-peer rating)
* Aggregated rating system (avg + count)

---

### 🔔 Notification System

* Event-based notifications:

  * Request sent
  * Request accepted/rejected
  * Extension updates
* Linked navigation support
* User-specific notification feed

---

### 📊 Dashboard API

* Aggregated stats:

  * Active borrows (lent & borrowed)
  * Pending requests
  * Overdue records
* Optimized using aggregation queries

---

### 🔍 Filtering, Search & Ordering

* DjangoFilterBackend integration
* Search across title and author
* Ordering support (e.g. created_at)
* Clean query-based filtering

---

### 📄 API Documentation

* Swagger/OpenAPI integration (drf-yasg)
* Interactive API testing interface
* Well-structured endpoints

---

## 🏗️ Tech Stack

* **Backend:** Django, Django REST Framework
* **Database:** PostgreSQL
* **Authentication:** JWT (SimpleJWT / Djoser)
* **Media Storage:** Local / Cloudinary / S3 (configurable)
* **Documentation:** Swagger (drf-yasg)

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/mohsin105/Book_Bridge
cd bookbridge-backend
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Setup Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_db_url
FRONTEND_URL=http://localhost:3000
```

---

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

---

### 7. Run Server

```bash
python manage.py runserver
```

---

## 📌 API Endpoints Overview

| Module          | Endpoint                                      |
| --------------- | -------------------------------               |
| Auth            | `/api/auth/`                                  |
| Books           | `/api/books/`                                 |
| Book Copies     | `/api/books/{book_pk}copies/`                 |
| Borrow Requests | `/api/borrow/requests/`                       |
| Borrow Records  | `/api/borrow/records/`                        |
| Extensions      | `/api/borrow/records/{id}/extensions/`        |
| Notifications   | `/api/notifications/`                         |
| Dashboard       | `/api/dashboard/stats/`                       |

---

## 🔄 Core Workflow

```text
User → Browse Books → Request Copy  
→ Owner Accepts → BorrowRecord Created  
→ Borrower Reads → Return / Extend  
→ System Handles Overdue & Fine
```

---

## 🧠 Key Design Decisions

* **Separation of Request and Record lifecycle**
* **Dynamic overdue detection (no background jobs)**
* **Soft delete for data integrity**
* **Role-based permissions (borrower vs owner)**
* **Nested relationships for contextual data**
* **Aggregation-based dashboard APIs**

---

## 📈 Future Improvements

* Real-time notifications (WebSockets)
* Geo-based book discovery
* Chat system between users
* Recommendation engine
* Mobile app integration

---

## 👨‍💻 Author

Developed as a fullstack-ready backend system demonstrating real-world architecture using Django + DRF.

---

## ⭐ Notes

This project is designed to simulate a **real-world peer-to-peer lending system**, going beyond basic CRUD by implementing:

* Complex workflows
* Role-based interactions
* Business logic constraints
* Scalable API design

---

## 📜 License

This project is for educational and portfolio purposes.

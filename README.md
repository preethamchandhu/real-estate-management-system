# 🏠 Real Estate Management System

A full-stack **Real Estate Management System** built using **Django**, **MySQL**, and **MongoDB**. The application provides role-based access for **Admin**, **Agent**, and **Client**, enabling property management, transaction processing, document storage, and activity tracking.

---

## 🚀 Features

### 👨‍💼 Admin
- Dashboard with system statistics
- Manage users, properties, and transactions
- Monitor platform activities

### 🏡 Agent
- Add, edit, and delete property listings
- Upload property-related documents
- Approve or reject buy/rent requests
- Manage personal property listings

### 👤 Client
- Browse and search properties
- Request to buy or rent properties
- Track request status
- View property details

### 💾 Hybrid Database Architecture
- **MySQL**
  - User Management
  - Property Listings
  - Transactions

- **MongoDB**
  - Property Documents
  - Property Activity Logs

---

# 🛠️ Tech Stack

- Python
- Django
- MySQL
- MongoDB
- HTML5
- CSS3
- Bootstrap
- Git & GitHub

---

# 📂 Project Structure

```
realestate/
│
├── accounts/
├── properties/
├── transactions/
├── templates/
├── static/
├── realestate/
└── manage.py
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/preethamchandhu/real-estate-management-system.git
cd real-estate-management-system
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure MySQL

Create a database named:

```sql
CREATE DATABASE realestate_db;
```

Update your database settings in `realestate/settings.py` or use environment variables.

---

## 5. Configure MongoDB

Start MongoDB locally.

Default configuration:

```text
MONGO_URI = mongodb://localhost:27017/
MONGO_DB_NAME = realestate_mongo
```

---

## 6. Apply Migrations

```bash
python manage.py migrate
```

---

## 7. Create Superuser

```bash
python manage.py createsuperuser
```

---

## 8. Load Demo Data (Optional)

```bash
python manage.py seed_demo
```

Demo Accounts

| Role | Username | Password |
|------|----------|----------|
| Agent | demo_agent | Demo@12345 |
| Client | demo_client | Demo@12345 |

---

## 9. Run Server

```bash
python manage.py runserver
```

Open

```
http://127.0.0.1:8000/
```

---

# 🔄 Application Workflow

1. Register as Agent or Client
2. Agent adds property listings
3. Client browses available properties
4. Client submits Buy/Rent request
5. Agent approves or rejects request
6. Property documents are stored in MongoDB
7. Property activities are logged in MongoDB

---

# 📊 Database Architecture

### MySQL

- Users
- Properties
- Transactions

### MongoDB

- Property Documents
- Activity Logs

---

# ✨ Key Highlights

- Hybrid Database Architecture (MySQL + MongoDB)
- Role-Based Authentication
- CRUD Operations
- Property Search & Filtering
- Transaction Management
- Responsive UI
- Activity Logging
- Document Management

---

# 📸 Screenshots

Add screenshots of:

- Home Page
- Admin Dashboard
- Agent Dashboard
- Client Dashboard
- Property Details
- Add Property
- MongoDB Collections

---

# 👨‍💻 Author

**Preetham Chandhu**

- GitHub: https://github.com/preethamchandhu
- LinkedIn: https://www.linkedin.com/in/preethamchandhur

---

⭐ If you found this project useful, consider giving it a Star.
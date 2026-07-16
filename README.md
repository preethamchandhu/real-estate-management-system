# Real Estate Transaction & Property Management System

Django + MySQL (relational data) + MongoDB (unstructured docs/activity log) web app
with 3 roles: **Admin**, **Agent**, **Client**.

## Features
- Custom user model with roles (admin / agent / client)
- Agents: list, edit, delete properties; upload supporting documents (stored in MongoDB); approve/reject buy-rent requests
- Clients: browse/search properties, request to buy/rent, track request status
- Admin: full Django admin panel + dashboard with stats
- Hybrid DB: MySQL for Users/Properties/Transactions, MongoDB for property documents & activity log

## 1. Prerequisites
- Python 3.10+
- MySQL Server running locally
- MongoDB Server running locally (optional — app still runs without it, just skips document/activity features)

## 2. Setup

```bash
# from the project root
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## 3. Create the MySQL database

```sql
CREATE DATABASE realestate_db CHARACTER SET utf8mb4;
```

## 4. Configure environment variables (or edit realestate/settings.py directly)

```bash
export MYSQL_DB=realestate_db
export MYSQL_USER=root
export MYSQL_PASSWORD=yourpassword
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MONGO_URI=mongodb://localhost:27017/
export MONGO_DB_NAME=realestate_mongo
```
(On Windows, use `set VAR=value` instead of `export`.)

## 5. Run migrations & create an admin user

```bash
python3 manage.py migrate
python3 manage.py createsuperuser
```
When creating the superuser, Django will still ask for username/email/password.
After creation, set that user's `role` to `admin` via `/admin/` (or the shell) —
superusers already bypass role checks, so this is optional but keeps things consistent.

## 6. (Optional) Load demo data

Populate the app with a demo agent, a demo client, 6 sample Bengaluru listings
(with generated placeholder images), and one sample pending request:

```bash
python3 manage.py seed_demo
```

```
Agent login:  demo_agent / Demo@12345
Client login: demo_client / Demo@12345
```

Safe to re-run — it skips anything that already exists.

## 7. Run the server

```bash
python3 manage.py runserver
```

Visit http://127.0.0.1:8000/

- `/` — browse properties (public)
- `/accounts/register/` — sign up as Agent or Client
- `/admin/` — Django admin (for the superuser you created)
- `/dashboard/` — role-based dashboard after login

## 8. Typical flow to test
1. Register one user as **Agent**, another as **Client** (two browser sessions/incognito, or logout/login).
2. As Agent: add a property from the dashboard.
3. As Client: browse to the property, click "Request to Buy/Rent".
4. As Agent: go to "Requests", approve or reject it.
5. Optionally, as Agent on a property's detail page, add a supporting document — this is stored in MongoDB and shown below the listing.

## Project structure
```
realestate/          # project settings & root urls
accounts/            # custom User model, auth, dashboards
properties/          # Property model, MySQL CRUD + MongoDB doc/activity helper (mongo.py)
transactions/         # Transaction model (buy/rent requests + approval flow)
templates/            # all HTML templates
static/css/style.css  # styling
```

## Notes
- If MongoDB isn't running, the app degrades gracefully — property pages and everything else still work, only the "Supporting Documents"/"Activity Log" sections stay empty.
- `DEBUG = True` and `SECRET_KEY` in `settings.py` are dev defaults — change both before deploying anywhere public.

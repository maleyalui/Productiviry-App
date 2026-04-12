#  Productivity Journal API

##  Project Title

**Productivity Journal API**

---

##  Project Description

This is a RESTful API built using Flask that allows users to manage personal journal entries. Users can sign up, log in, and perform CRUD (Create, Read, Update, Delete) operations on their journal entries. Each entry can include a title, content, and mood, helping users track productivity and emotional patterns over time.

The API uses session-based authentication and supports pagination for efficient data retrieval.

---

##  Installation Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Productiviry-App
```

### 2. Install Pipenv (if not installed)

```bash
pip install pipenv
```

### 3. Install dependencies

```bash
pipenv install
```

### 4. Activate virtual environment

```bash
pipenv shell
```

### 5. Set environment variables

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
```

### 6. Initialize database migrations

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 7. Seed the database

```bash
python seed.py
```

---

## ▶️ Run Instructions

Start the development server:

```bash
flask run
```

Server will run on:

```bash
http://127.0.0.1:5000
```

---

##  API Endpoints

###  Authentication

#### 1. Signup

* **POST /signup**
* Creates a new user
* **Body:**

```json
{
  "username": "string",
  "password": "string"
}
```

---

#### 2. Login

* **POST /login**
* Logs in a user and creates a session

---

#### 3. Logout

* **DELETE /logout**
* Logs out the current user

---

#### 4. Check Session

* **GET /check_session**
* Returns the currently logged-in user

---

###  Journal Entries

#### 5. Get All Entries

* **GET /journals**
* Returns paginated journal entries for the logged-in user
* **Query Params:**

  * `page` (default: 1)
  * `per_page` (default: 10)

---

#### 6. Create Entry

* **POST /journals**
* Creates a new journal entry
* **Body:**

```json
{
  "title": "string",
  "content": "string",
  "mood": "string"
}
```

---

#### 7. Get Single Entry

* **GET /journals/<id>**
* Returns a specific journal entry

---

#### 8. Update Entry

* **PATCH /journals/<id>**
* Updates a journal entry

---

#### 9. Delete Entry

* **DELETE /journals/<id>**
* Deletes a journal entry

---

##  Pipfile (Dependencies)

```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
flask = "*"
flask-restful = "*"
flask-sqlalchemy = "*"
flask-migrate = "*"
flask-bcrypt = "*"
faker = "*"

[dev-packages]

[requires]
python_version = "3.12"
```

---

##  Test Files

Currently, no automated tests are implemented.

### Suggested Improvements:

* Use `pytest` for unit and integration testing
* Add tests for:

  * Authentication (signup/login)
  * Journal CRUD operations
  * Authorization checks

---

##  Author

**Luis Maleya**

---

## Future Enhancements

* JWT-based authentication
* Frontend integration (React)
* Tagging and categorization for journal entries
* Search and filtering functionality
* Deployment (Render / Railway / AWS)

---

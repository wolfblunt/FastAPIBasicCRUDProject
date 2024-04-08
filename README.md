# Backend FastAPI

## My Awesome FastAPI Project

This is a simple REST API built with Python and FastAPI and SQLAlchemy for CRUD operations (Create, Read, Update, Delete) on Students.
FastAPI is a powerful web framework for building APIs.

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
venv\Scripts\activate
uvicorn main:app --reload
```

The application will start and be available at http://localhost:8000.

## API Endpoints

### Retrieve a list of students:

```http
GET /students
```

Returns a list of all students in the system:

```console
curl http://localhost:8000/students/ -H "Accept: application/json"
```
Response:

```json
[
    {
        "id": "7a2d72f9e92d4231ac6dd834aa7461d1",
        "name": "Jai",
        "age": 26,
        "address": 
        {
            "city": "Delhi",
            "country": "India"
        }
    },
    {
        "id": "4a1dddb9d74e427d9f8e6fdbe2e112a2",
        "name": "Adi",
        "age": 20,
        "address": 
        {
            "city": "Jaipur",
            "country": "India"
        }
    },
    {
        "id": "95f3bee04dad487eb54ae61a457201ea",
        "name": "Anuj",
        "age": 23,
        "address": 
        {
          "city": "Pune",
          "country": "India"
        }
    }
]
```

### Retrieve details for a specific user:

```http
GET /students/{user_id}
```
Returns details for a specific user with the given user_id:

```console
curl http://localhost:8000/students/95f3bee04dad487eb54ae61a457201ea -H "Accept: application/json"
```
Response:
```json
{
        "id": "95f3bee04dad487eb54ae61a457201ea",
        "name": "Anuj",
        "age": 23,
        "address": 
        {
          "city": "Pune",
          "country": "India"
        }
}
```

### Add a new user

```http
POST /students
```

API to create a student in the system. All fields are mandatory and required while creating the student in the system.

  - `name` (string, required): the name of the user
  - `age` (string, required): the email address of the user
  - `address` (string, required): the address for the user which includes city and country.

```console
curl -X POST http://localhost:8000/students/
   -H 'Content-Type: application/json'
   -d '{
    "age": 31,
    "name": "Shyam",
    "address":
        {
            "country": "Japan",
            "city": "Tokyo"
        }
    }'
```
Response:

```json
{
  "id": "34c8b3111bf34e1f8fbff33cb6b0a593"
}
```


### Update an existing user
```http
PATCH /students/{user_id}
```

Updates an existing user with the given user_id. The request body should include a JSON object with the following properties:

  -  `name` (string): the new name for the user
  -  `age` (int): the new age for the user
  -  `city` (string): the new city for the user
  -  `country` (string): the new country for the user

```console
curl -X PUT http://localhost:8000/students/95f3bee04dad487eb54ae61a457201ea
     -H "Accept: application/json"
     -d '{"age": 24, "address":{"city": "Jaipur"}}'
```
Response:
```json
{}
```

### Delete a user

```http
DELETE /students/{user_id}
```

Deletes the user with the given user_id:

```console
curl -X DELETE http://localhost:8000/{student_id}
```

Response:
```json
{}
```


## Code credit

Code credits for this code go to [Aman Khandelwal](https://github.com/wolfblunt)
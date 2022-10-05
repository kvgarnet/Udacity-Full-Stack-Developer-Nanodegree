# Full Stack Trivia API Backend

The Full Stack Trivia is offered to you as a RESTful API running on a Python based FLASK server.

Follow below instruction or head down to the [API documentation](#api-documentation) to see what this powerful Trivia API is capable of.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Activate  virtual environment by writing:

source env/bin/activate (on Mac or Linux - see docs for Windows instructions)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
for flask version 2.2 +, just run
```
flask --app flaskr --debug run
```
Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

# API Documentation

This describes the resources that make up the official Full Stack Trivia API, which allows for easy integration of the trivia functionality into any web or mobile application.

## Base URL
Since this API is not hosted on a specific domain, it can only be accessed when flask is run locally. To make requests to the API via curl or postman, you need to use the default domain on which the flask server is running.

http://127.0.0.1:5000/



## Endpoints
* GET '/categories'
* GET '/questions?page={page_number}'
* POST '/questions'
* DELETE '/questions/{question_id}'
* POST '/questions/search'
* GET '/categories/{category_id}/questions'
* POST '/quizzes'

### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An dict object with key "categories" containing:
  - an dictionary with below key:value pairs:
    - "id": String
    - "type": String 

fetch example: 
```
curl "localhost:5000/categories"                                                                                                                              
```
response
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

### Get '/questions?page={page_number}'
- Fetches a list of questions for all categories paginated with 10 questions per page
- Request Arguments:
  - Query string params: Page number as Integer (optional: not submitted by default, will output all result)
- Returns: JSON object with keys: 
    - "categories": list of dict as above
    - "current_category": null
    - "questions": list of dict 
    - "total_questions": integer
    - "success": boolean
  
example:
```
 curl "http://localhost:5000/questions?page=2" 
 ```
response
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "current_category": "Geography",
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "swimming",
      "category": 2,
      "current_category": "Art",
      "difficulty": 1,
      "id": 32,
      "question": "what is your favorite fsport?"
    }
  ],
  "success": true,
  "total_questions": 17
}
```

### POST '/questions/'
- Creates a new question
- Request Arguments:
  - Body: JSON Object containing "question": String, "answer": String, "difficulty": Int (1-5), "category": Int
- Returns:
  - Body: JSON Object containing:
    - "questions": list of dict 
    - "category": string
    - "new_question_id": integer
    - "total_questions": integer
    - "success": boolean
  
example 
```
curl localhost:5000/questions -X POST -d '{"question":"what is your favorite sport?","answer":"table tennis","category":2,"difficulty":1}' -H "Content-Type:application/json"
```
response
```
{
  "category": 2,
  "new_question_id": 33,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "swimming",
      "category": 2,
      "difficulty": 1,
      "id": 32,
      "question": "what is your favorite fsport?"
    },
  ],
  "success": true,
  "total_questions": 18
}
```

### DELETE '/questions/{question_id}'
- Deletes question with question_id from database
- Request Arguments:
  - URL Params: Question ID as Int
- Returns: 
  - Body: JSON Object containing:
    - "deleted_question_id": string 
    - "questions": list of dict
    - "total_questions": integer
    - "success": boolean
    
example
```
curl "http://localhost:5000/questions/24" -X DELETE                                                          
```
response
```
{
  "deleted_question_id": "24",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "current_category": "Entertainment",
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    ...omitted...
    {
      "answer": "table tennis",
      "category": 2,
      "current_category": "Art",
      "difficulty": 1,
      "id": 33,
      "question": "what is your favorite sport?"
    }
  ],
  "success": true,
  "total_questions": 17
}
```

### POST '/questions/search'
- Fetches a list of questions for a given search term among all categories paginated with 10 questions per page
- Request Arguments:
  - Query string params: Page number as Integer (optional)
  - Body: JSON object with "search_tern": String
```
{
  "searchTerm": "Tom Hanks",
}
```
- Returns: 
  - Body: JSON Object containing:
    - "questions": list of dict
    - "total_questions": integer
    - "success": boolean
    - "current_category": null
  
example:
```
curl localhost:5000/questions/search -X POST -d '{"searchTerm":"title"}' -H "Content-Type:application/json"

```
response
```
{
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "current_category": "History",
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "current_category": "Entertainment",
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

### GET '/categories/{category_id}/questions'
- Fetches a list of all questions for a particular category
- Request Arguments:
  - Query string params: Category id as Integer
- Returns: 
  - Body: JSON Object containing:
    - "questions": list of dict
    - "total_questions": integer
    - "success": boolean
    - "current_category": integer
  
example:
```
 curl "localhost:5000/categories/6/questions"
```
response
```
{
  "current_category": 6,
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```
### POST '/quizzes'
- Fetches question to play the quiz
- Request Arguments:
  - Body: JSON object with "previous_questions": Array of Integers, "quiz_category": JSON object with "type": String, "id": Int
```
{
  "previous_questions":[],
  "quiz_category":{"type":"click","id":0}
}
```
- Returns: 
  - Body: JSON Object containing:
      - "questions": list of dict
      - "success": boolean
    
example
```
curl localhost:5000/quizzes -X POST -d '{"previous_questions": [],"quiz_category": {"type": "Art", "id": "2"}}' -H "Content-Type:application/json" 
```
response
```
{
  "question": {
    "answer": "Jackson Pollock",
    "category": 2,
    "difficulty": 2,
    "id": 19,
    "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
  },
  "success": true
}
```
## Status Codes

Trivia API returns the following status codes in its API:

| Status Code | Description |
| :--- | :--- |
| 200 | `Success` |
| 400 | `Bad Request` |
| 404 | `Resource Not Found` |
| 422 | `Unprocessable Entity` |

For all status codes a JSON object is included with a "success": Boolean and the correct data or error code and message.

```
{
  "error": 404, 
  "message": "Resource Not Found", 
  "success": false
}
```
## Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

### ENDPOINT
#### GET /categories
- General:
    - Return a list of quiz categories
    - curl http://127.0.0.1:5000/categories
  
```
{
  "categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertaiment",
    "Sports" 
  ]
}
```
#### GET /questions
- General:
  - Return a list of a questions objects, total questions, current category and categories. 
  - Return are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
  - `curl http://127.0.0.1:5000/questions?page=1`
  
```
{
    "categories": [
        "Science",
        "Art",
        "Geography",
        "History",
        "Entertainment",
        "Sports"
    ],
    "current_category": null,
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
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
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "total_questions": 21
}
```
    
#### POST /questions
- General:
  - Create new a question using the submitted question, answer, 
    category, and difficulty score. 
    Return the id of the created question, question(text), answer, category and difficulty.
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"answer": "Scarab","category": 1, "difficulty": 4, "question": "Which dung beetle was worshipped by the ancient Egyptians?"}'`    

```
{
  question: {
    'id': 1,
    'question': 'What is this application?',
    'answer': 'Trivia',
    'category': 'Entertainment',
    'difficulty': 1
  }
}
```
#### DELETE /questions/{question_id}
- General:
  - Delete the question of the given ID if it exists.
  Return success values.
  - `curl http://127.0.0.1:5000/questions/28 -X DELETE`  

```
{
  "sccess": true
}
```
#### POST /questions/search
- General:
  - Return a list of questions objects based on a search term, total questions, current category and categories.
  - `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "city"}'`

```
{
  'questions': [
    {
      'id': 15,
      'question': 'The Taj Mahal is located in which Indian city?',
      'answer': 'Agra',
      'category': 3,
      'difficulty': 2
    }
  ],
  'total_questions': 21,
  'current_category': None,
  'categories': [
    'Science',
    'Art',
    'Geography',
    'History',
    'Entertainment',
    'Sports'
  ]
}
```
#### GET /categories/{category_id}/questions
- General:
  - Return a list of question objects of the given category id, total questions, current category and categories if it exists.
  - `curl http://127.0.0.1:5000/categories/1/questions`
```
{
  'questions': [
    {
      'id': 10,
      'question': 'Which is the only team to play in every soccer World Cup tournament?',
      'answer': 'Brazil',
      'category': 6,
      'difficulty': 3
    },
    {
      'id': 11,
      'question': 'Which country won the first ever soccer World Cup in 1930?',
      'answer': 'Uruguay',
      'category': 6,
      'difficulty': 4
    }
  ],
  'total_questions': 21,
  'current_category': None,
  'categories': [
    'Science',
    'Art',
    'Geography',
    'History',
    'Entertainment',
    'Sports'
  ]
}
```
#### POST /quizzes
- General:
  - Return a random question object using submitted previous_questions, quiz_category id and type.
  - `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category":{"id":1, "type":"Art"}}'`
  
```
{
  'id': 12,
  'question': 'Who invented Peanut Butter?',
  'answer': 'George Washington Carver',
  'category': 4,
  'difficulty': 2
}
```
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

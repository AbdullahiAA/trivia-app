# Trivia APP

This project is one of the projects that I'm proud of. Basically, this project is a platform that allows users to post different questions based on different types of categories. i.e Science, Art, Entertainment, Sports and so on. This trivia app also allows users to attempt quizzes on there chosen category or all the categories.

## Getting Started

### Pre-requisites and Local Development

Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file.

To run the application run the following commands:

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.

#### Frontend

From the frontend folder, run the following commands to start the client if you're using npm:

```
npm install // only once to install dependencies
npm start
```

Run this if you're using yarn:

```
yarn // Only once to install all the dependencies
yarn start
```

By default, the frontend will run on localhost:3000.

### Tests

In order to run tests navigate to the backend folder and run the following commands:

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "status": False,
    "error": 400,
    "message": "Bad request"
}
```

The API will return five error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable
- 500: Server Error

#### Fetch all the categories

#### GET /categories

- General:
  - Returns the list of the available categories
- Sample: `curl http://127.0.0.1:5000/categories`

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

#### Fetch all the questions

#### GET /questions

- General:
  - Returns a list of questions, categories and the total number of questions
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/questions`
- Sample (including the page): `curl http://127.0.0.1:5000/questions?page=2`

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
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ],
  "total_questions": 23
}
```

#### Fetch questions by category

#### GET /categories/{category_id}/questions

- General:
  - Returns a list of questions based on the specified category.
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`
- Sample (including the page): `curl http://127.0.0.1:5000/categories/1/questions?page=2`

```
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "total_questions": 3
}
```

#### Add a new question

#### POST /questions

- General:
  - Creates a new question using the submitted question, answer, category ID and difficulty (Ranging from 1 - 5).
- `curl http://127.0.0.1:5000/questions?page=3 -X POST -H "Content-Type: application/json" -d '{"question": "What is the name of the president of Nigeria?", "answer": "Gen. Muhammad Buhari", "category": 4, "difficulty": 1}'`

Body data

```
{
    "question": "What is the name of the president of Nigeria?",
    "answer": "Gen. Muhammad Buhari",
    "category": 4,
    "difficulty": 1
}
```

Response

```
{
  "message": "Question added successfully.",
  "status": true
}
```

#### Search for question(s)

#### POST /questions/search

- General:
  - Search for questions that matched the submitted search term.
- `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}'`

Body data

```
{
   "searchTerm": "title"
}
```

Response

```
{
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "total_questions": 2
}
```

#### Delete a question

#### DELETE /questions/{question_id}

- General:
  - Deletes the question of the given ID if it exists.
- `curl -X DELETE http://127.0.0.1:5000/questions/23`

Response

```
{
  "message": "Question deleted successfully.",
  "status": true
}
```

#### Fetch a quiz question

#### POST /quizzes

- General:
  - Fetch a quiz question based on the choosing category or all categories if the `quiz_category` is not specified
- `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{ "previous_questions": [1, 3, 18], "quiz_category": { "id": 5, "type": "Science" }}'`

Body data

```
{
    "previous_questions": [1, 3, 18],
    "quiz_category": {
        "id": 5,
        "type": "Science"
    }
}
```

Response

```
{
  "question": {
    "answer": "Edward Scissorhands",
    "category": 5,
    "difficulty": 3,
    "id": 6,
    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  }
}
```

## Deployment N/A

## Author

Yours truly, Jelili Abdullahi

## Acknowledgements

To the awesome coach, Coach Caryn and the entire team of ALX-T and Udacity!

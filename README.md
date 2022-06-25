# Trivia APP

This project is one of the project that I'm proud for. Basically, this project is a platform that allows users to post differen questions based on different types of categories. i.e Science, Art, Entertainment, Sports and so on. This trivia app also allows users to attempt quizzes on there chosen category.

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
      "answer": "Engine",
      "category": 4,
      "difficulty": 1,
      "id": 35,
      "question": "What is that?"
    },
    {
      "answer": "Gen. Muhammad Buhari",
      "category": 4,
      "difficulty": 1,
      "id": 36,
      "question": "What is the name of the president of Nigeria?"
    },
    {
      "answer": "Gen. Muhammad Buhari",
      "category": 4,
      "difficulty": 1,
      "id": 37,
      "question": "What is the name of the president of Nigeria?"
    }
  ],
  "total_questions": 23
}
```

## Deployment N/A

## Authors

Yours truly, Jelili Abdullahi

## Acknowledgements

To the awesome coach, Coach Caryn and the entire team of ALX-T and Udacity!

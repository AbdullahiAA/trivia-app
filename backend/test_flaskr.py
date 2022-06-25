import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

from dotenv import load_dotenv
load_dotenv()


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.DB_HOST = os.getenv('DB_HOST')
        self.DB_USER = os.getenv('DB_USER')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD')
        self.DB_TEST_NAME = os.getenv('DB_TEST_NAME')

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = self.DB_TEST_NAME
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(
            self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_TEST_NAME)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            "answer": "Gen. Muhammad Buhari",
            "question": "What is the name of the president of Nigeria?",
            "difficulty": 1,
            "category": 4
        }

        self.valid_quiz_data = {
            "previous_questions": [1, 3, 18],
            "quiz_category": {
                "id": 5,
                "type": "Science"
            }
        }

        self.invalid_quiz_data = {
            # "previous_questions": [1, 3, 18],
            "quiz_category": {
                "id": 5,
                "type": "Science"
            }
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    def test_404_get_categories(self):
        res = self.client().get('/categories/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_404_get_beyond_valid_pages(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_delete_question(self):
        res = self.client().delete('/questions/22')
        data = json.loads(res.data)

        # Get the deleted question
        question = Question.query.get(22)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], True)
        self.assertEqual(data['message'], 'Question deleted successfully.')
        self.assertEqual(question, None)

    def test_404_delete_an_invalid_question(self):
        res = self.client().delete('/books/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_add_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['status'], True)
        self.assertEqual(data['message'], 'Question added successfully.')

    def test_400_add_question_with_no_data(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_405_add_question_via_invalid_route(self):
        res = self.client().post('/questions/21', json={**self.new_question})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['status'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    def test_search_for_question_on_match(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm': 'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 2)
        self.assertEqual(data['total_questions'], 2)

    def test_search_for_question_on_no_match(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm': 'redbull'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)

    def test_search_for_question_with_no_search_term(self):
        res = self.client().post('/questions/search', json={'searchTerm': ''})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], False)
        self.assertEqual(
            data['message'], 'Please type something and try again')

    def test_search_for_question_with_no_body(self):
        res = self.client().post('/questions/search', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        category = Category.query.get(2).format()['type']

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], category)

    def test_get_questions_by_invalid_category(self):
        res = self.client().get('/categories/200/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], False)
        self.assertEqual(data['message'], 'Unknown category selected')

    def test_requesting_beyond_available_questions_by_category(self):
        res = self.client().get('/categories/2/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_get_quiz_question(self):
        res = self.client().post('/quizzes', json=self.valid_quiz_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])

    def test_get_quiz_question_on_invalid_data(self):
        res = self.client().post('/quizzes', json=self.invalid_quiz_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], False)
        self.assertEqual(data['message'], 'Bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

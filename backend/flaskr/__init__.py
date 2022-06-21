import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, questions):
    # Calculate the start and the end of the questions based on the page
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    return questions[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    # cors = CORS(app, resources={r"*/api/*": {"origin": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    # @app.after_request
    # def after_request(response):
    #     response.headers.add(
    #         "Access-Control-Allow-Headers", "Content-Type, Authorization"
    #     )
    #     response.headers.add(
    #         "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
    #     )

    #     return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]

        return jsonify({
            'categories': formatted_categories
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        questions = Question.query.all()

        formatted_questions = [question.format() for question in questions]

        categories = [category.format() for category in Category.query.all()]

        return jsonify({
            'questions': paginate_questions(request, formatted_questions),
            'total_questions': len(formatted_questions),
            'categories': categories,
            # 'current_category': current_category
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)

        # Abort if no question is found
        if question == None:
            abort(404)

        question.delete()

        return jsonify({
            'status': True,
            'message': 'Question deleted successfully.'
        })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def add_question():
        question = request.json['question']
        answer = request.json['answer']
        difficulty = request.json['difficulty']
        category = request.json['category']

        # Handle when any of the field is not supplied
        if question == None or answer == None or difficulty == None or category == None:
            return jsonify({
                'status': False,
                'message': 'All fields are required'
            })

        new_question = Question(
            question=question,
            answer=answer,
            difficulty=difficulty,
            category=category
        )

        Question.insert(new_question)

        return jsonify({
            'status': True,
            'message': 'Question added successfully',
        })

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        search_term = request.json['searchTerm'].strip()

        if search_term is None or search_term == "":
            return jsonify({
                'status': False,
                'message': 'Please type something and try again'
            })

        related_questions = Question.query.filter(
            func.lower(Question.question).like("%{}%".format(search_term.lower()))).all()

        formatted_questions = [question.format()
                               for question in related_questions]

        return jsonify({
            'message': search_term,
            'questions': formatted_questions,
            'total_questions': len(formatted_questions),
            # 'current_category': current_category
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        current_category = Category.query.get(category_id)

        # Handle when an invalid category is selected
        if current_category == None:
            return jsonify({
                'status': False,
                'message': 'Unknown category selected'
            })
        else:
            # Format the current category
            current_category = current_category.format()

        # Fetch the questions based on the category selected
        questions = Question.query.filter_by(
            category=category_id).all()

        # Handle when the category selected has no questions
        if questions == None:
            return jsonify({
                'questions': [],
                'total_questions': 0,
                'current_category': current_category
            })

        formatted_questions = [question.format() for question in questions]

        return jsonify({
            'questions': paginate_questions(request, formatted_questions),
            'total_questions': len(formatted_questions),
            'current_category': current_category
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        previous_questions = request.json['previous_questions']
        quiz_category = request.json['quiz_category']

        # Fetch all the questions if category is not specified
        if quiz_category == None or quiz_category == "":
            questions = Question.query.all()
        else:
            # Fetch questions based on category
            questions = Question.query.filter_by(
                category=quiz_category['id']).all()

        available_questions = filter(
            lambda q: q.id not in previous_questions, questions)
        available_questions = list(available_questions)

        if len(available_questions) == 0:
            return jsonify({
                'status': False,
                'message': 'No questions available'
            })

        random_question = random.choice(available_questions)

        print(questions)
        print(available_questions)
        print(random_question)

        return jsonify({
            'previous_questions': previous_questions,
            'quiz_category': quiz_category,
            'question': random_question.format(),
        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

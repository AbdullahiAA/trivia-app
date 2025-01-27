import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, questions):
    # Calculate the start and the end of the questions based on the page
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    return questions[start:end]


def format_category(categories):
    category_list = [category.format() for category in categories]
    formatted_categories = {cat['id']: cat['type'] for cat in category_list}

    return formatted_categories


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"*": {"origins": "*"}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )

        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        try:
            categories = Category.query.all()
            formatted_categories = format_category(categories)

            return jsonify({
                'categories': formatted_categories
            })
        except:
            abort(404)

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
        paginated_questions = paginate_questions(request, formatted_questions)

        if len(paginated_questions) == 0:
            abort(404)

        categories = Category.query.all()
        formatted_categories = format_category(categories)

        return jsonify({
            'questions': paginated_questions,
            'total_questions': len(formatted_questions),
            'categories': formatted_categories,
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
        question = question.format()

        return jsonify({
            'status': True,
            'message': 'Question deleted successfully.',
            'question_id': question['id']
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
            }), 400

        new_question = Question(
            question=question,
            answer=answer,
            difficulty=difficulty,
            category=category
        )

        new_question.insert()

        return jsonify({
            'status': True,
            'message': 'Question added successfully.',
        }), 201

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
        try:
            search_term = request.json['searchTerm'].strip()

            if search_term is None or search_term == "":
                return jsonify({
                    'status': False,
                    'message': 'Please type something and try again',
                }), 400

            related_questions = Question.query.filter(
                Question.question.ilike("%{}%".format(search_term.lower()))).all()

            formatted_questions = [question.format()
                                   for question in related_questions]

            return jsonify({
                'questions': formatted_questions,
                'total_questions': len(formatted_questions),
            })
        except:
            abort(400)

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
            }), 400

        # Format the current category
        current_category = current_category.format()

        # Fetch the questions based on the category selected
        questions = Question.query.filter_by(
            category=category_id).all()
        formatted_questions = [question.format() for question in questions]
        paginated_questions = paginate_questions(request, formatted_questions)

        # Handle when the category selected has no questions
        if len(paginated_questions) == 0:
            abort(404)

        return jsonify({
            'questions': paginated_questions,
            'total_questions': len(formatted_questions),
            'current_category': current_category['type']
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
        body = request.get_json()

        try:
            previous_questions = body.get('previous_questions', None)
            quiz_category = body.get('quiz_category', None)

            if previous_questions is None:
                abort(404)

            # Fetch all the questions if category is not specified
            if quiz_category == None or quiz_category['id'] == 0:
                questions = Question.query.all()
            else:
                # Fetch questions based on category
                questions = Question.query.filter_by(
                    category=quiz_category['id']).all()

            # Filter out the previous_questions
            available_questions = filter(
                lambda q: q.id not in previous_questions, questions)
            available_questions = list(available_questions)

            if len(available_questions) == 0:
                return jsonify({
                    'status': False,
                    'message': 'No questions available'
                })

            # Choose a random question from the available questions
            random_question = random.choice(available_questions)

            return jsonify({
                'question': random_question.format()
            })
        except:
            abort(400)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(_error):
        return jsonify({
            'status': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'status': False,
            'error': 404,
            'message': 'Not found',
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'status': False,
            'error': 405,
            'message': 'Method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'status': False,
            'error': 422,
            'message': 'Unprocessable entity'
        }), 422

    @app.errorhandler(500)
    def server_error(_error):
        return jsonify({
            'status': False,
            'error': 500,
            'message': 'Server error'
        }), 500

    return app

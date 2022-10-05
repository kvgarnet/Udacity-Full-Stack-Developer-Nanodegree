import os,json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
def paginate_display(request,queries):
    formatted_display = [query.format() for query in queries]
    #set default value if param "page" NOT sent via request's args
    page = request.args.get("page", 1, type=int)
    # if "page' sent via request args , display paginated
    if request.args.get("page"):
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        return formatted_display[start:end]
    # else,display all
    return formatted_display
#embed current_category type in each question
def get_current_category(queries):
    current_category_question_lst=[]
    for q in queries:
        q['current_category'] = Category.query.get(q.get('category')).type
        current_category_question_lst.append(q)
    return current_category_question_lst
#format categories output based on frontend requirement
def format_categories(queries):
    format_category = {}
    for c in queries:
        format_category[str(c.id)] = c.type
    return format_category


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    #basic, enable every URL to allow CORS
    # CORS(app)
    #enable CORS for specific api,we alllow all (/*)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
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
            categories = Category.query.order_by('id').all()
        except:
            abort(422)
        # if categories not found
        if not categories:
            abort(404)
        # else return
        return jsonify({
            'success': True,
            'categories': format_categories(categories)
            # 'categories': paginate_display(request, categories)
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
    # currentCategory for this endpoint can be None for all questions
    # https: // knowledge.udacity.com / questions / 82424

    @app.route('/questions')
    def get_questions():
        try:
            questions = Question.query.order_by(Question.id).all()
            categories = Category.query.order_by(Category.id).all()
        except:
            abort(422)
        # Paginate list of questions and make sure it is a valid page
        questions_paginated = paginate_display(request, questions)

        if not questions_paginated:
            abort(404)
        # else return
        # TBD: current_category should be not be returned on top level
        # better to be embedded in each question's dictionary?
        return jsonify({
            'success': True,
            'questions': get_current_category(questions_paginated),
            'total_questions': len(questions),
            'categories': format_categories(categories),
            # 'categories': [category.format() for category in categories],
            'current_category': None
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
        error = False
        question = Question.query.get(question_id)
        if not question:
            abort(404)

        try:
            question.delete()
            questions = Question.query.order_by('id').all()
            question_page_lst = paginate_display(request, questions)
            total_questions = len(Question.query.all())
            return jsonify({
                'success': True,
                'deleted_question_id': question_id,
                'questions': get_current_category(question_page_lst),
                'total_questions': total_questions
            })
        except:
            question.rollback()
            print(sys.exc_info())
            return abort(422)
        finally:
            question.close()


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
    def post_question():
        body = request.get_json()
        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)
        # Check if required fields submitted
        if not (question and answer and difficulty and category):
            abort(422)
        try:
            question = Question(
                question=question,
                answer=answer,
                difficulty=difficulty,
                category=category)
            question.insert()
            questions = Question.query.order_by('id').all()
            questions_page_lst = paginate_display(request,questions)
            total_questions = len(Question.query.all())
            return jsonify({
                'success': True,
                'new_question_id': question.id,
                'category': question.category,
                'questions': questions_page_lst,
                'total_questions': total_questions
            })
        except:
            question.rollback()
            print(sys.exc_info())
            return abort(422)
        finally:
            question.close()

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
        search_term = request.get_json().get('searchTerm', '')
        print(f"search item is: {search_term}")
        ilike_search = f'%{search_term}%'
        questions = Question.query.order_by(Question.id).filter(Question.question.ilike(ilike_search)).all()
        if len(questions) == 0:
            abort(404)
        questions_page_lst = paginate_display(request, questions)
        return jsonify({"success": True,
                        "questions": get_current_category(questions_page_lst),
                        "total_questions": len(questions_page_lst),
                        'current_category': None
                        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_per_category(category_id):
        print(f"cat id:{category_id}")
        questions = Question.query.order_by(Question.id).filter(Question.category == category_id).all()
        print(f"question per category is: {questions}")
        if len(questions) == 0:
            abort(404)
        questions_page_lst = paginate_display(request, questions)
        return jsonify({
                        "success": True,
                        "questions": questions_page_lst,
                        "total_questions": len(questions_page_lst),
                        'current_category': category_id
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
    def get_quiz_questions():
        body = request.get_json()
        if not ('quiz_category' in body and 'previous_questions' in body):
            abort(422)
        category = body.get('quiz_category', None)
        previous_questions = body.get('previous_questions', None)
        print(f"category is: {category}")
        print(f"pre question is: {previous_questions}")
        if category['type'] == 'click':
            questions = Question.query.order_by(Question.id).filter(Question.id.notin_(previous_questions)).all()
        else:
            questions = Question.query.order_by(Question.id).filter_by(category = str((category['id'])))\
                    .filter(Question.id.notin_(previous_questions)).all()
        # print(f"questions is {questions}")
        quiz_question=random.choice(questions).format() if questions else None
        return jsonify({"question": quiz_question,
                        "success": True
                        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def error_bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def error_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify(
            {
                'success': False,
                'error': 405,
                'message': "Method not allowed"
            }
        ),405
    @app.errorhandler(422)
    def error_unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(500)
    def server_internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Server Internal Error"
        }), 500

    return app


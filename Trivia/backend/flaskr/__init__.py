import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
def paginate_display(request,queries):
    formatted_display = [query.format() for query in queries]
    #set defalut for  if param "page" NOT sent via request's args
    page = request.args.get("page", 1, type=int)
    if request.args.get("page"):
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        return formatted_display[start:end]
    #display all
    return formatted_display
#embed current_category type name in each question
def get_current_category(queries):
    current_category_question_lst=[]
    for q in queries:
        d = q
        d['current_category'] = Category.query.filter(Category.id == q.get('category')).one_or_none().type
        current_category_question_lst.append(d)
    return current_category_question_lst
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

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
            'categories': paginate_display(request,categories)
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
            'totalQuestions': len(questions),
            'categories': paginate_display(request,categories),
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
        question = Question.query.filter(Question.id == question_id).one_or_none()
        if question is None:
            abort(404)
        try:
            question.delete()
            questions = Question.query.order_by('id').all()
            question_page_lst = paginate_display(request, questions)
            total_questions = len(Question.query.all())
        except:
            question.rollback()
            print(sys.exc_info())
            error = True
        finally:
            question.close()
        if error:
            return abort(422)
        else:
            return jsonify({
                'success': True,
                'deleted_question_id': question_id,
                'questions': question_page_lst,
                'total_questions': total_questions
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
    def post_question():
        body = request.get_json()
        question = Question(
            question=body.get('question', None),
            answer=body.get('answer', None),
            difficulty=body.get('difficulty', None),
            category = body.get('category', None)
        )
        if not (question and answer and difficulty and category):
            abort(422)
        try:
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
        search_term = request.get_json().get('search', '')
        like_search = f'%{search_term}%'
        questions = Question.query.order_by(Question.id).filter(Question.question.ilike(like_search))
        print("\n~~~~~~~~~~~~~~~")
        print(f"search term: {search_term}")
        print("~~~~~~~~~~~~~~~")
        # if 'page' is set in URL, then display in pages
        questions_page_lst = paginate_display(request, questions)
        if len(questions_page_lst) == 0:
            abort(404)
        # else display all  matched
        return jsonify({"questions": questions_page_lst,
                        "success": True,
                        "match_questions_no": len(questions_page_lst),
                        'current_category': None
                        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

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

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app


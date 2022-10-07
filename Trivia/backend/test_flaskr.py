import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from settings import TEST_DB_NAME, DB_USER, DB_PASSWORD

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = TEST_DB_NAME
        self.database_path = "postgresql://{}:{}@{}/{}".format(
DB_USER,DB_PASSWORD, "localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {"question": "what is your name", "answer": "Neil Gaiman", "category": 2,"difficulty": 1}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # test category
    def test_get_categories(self):
        """Test get all categories """
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])
    def test_get_categories_not_found(self):
        res = self.client().get('/categories/1000')
        data = json.loads(res.data)
        # Ensuring data passes tests as defined below
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')
# test get questions
    def test_get_questions(self):
        """Test get all questions """
        res = self.client().get('/questions')
        data = json.loads(res.data)
        # print(f"data is :{data}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertEqual(data['total_questions'], len(data['questions']))

    def test_get_questions_not_found(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        # Ensuring data passes tests as defined below
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # test get questions per category
    def test_get_questions_category(self):
        res = self.client().get('/categories/6/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['current_category'],6)
        self.assertEqual(data['total_questions'], 2)

    def test_get_questions_category_not_found(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)
        print(f"category not found data is :{data}")
        # Ensuring data passes tests as defined below
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # test delete question
    def test_delete_question(self):
        # create a dummy question to be deleted
        dummy_question = Question(question='What is your favorite sports?',
                                  answer='swimming',
                                  difficulty=1,
                                  category=1)
        dummy_question.insert()
        dummy_question_id=dummy_question.id
        #delete dummy question
        res = self.client().delete(f'/questions/{dummy_question_id}')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == f'{dummy_question_id}').one_or_none()
        # print(f"question is :{question}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_question_id'],f'{dummy_question_id}')
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertEqual(question,None)

    def test_delete_question_not_found(self):
        res = self.client().delete('/questions/230000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

# test post questions
    def test_post_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        #rm newly created test question
        self.client().delete(f"/questions/{data['new_question_id']}")
        # print(f"delete question id: {data['new_question_id']}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_question_id'])

    def test_post_question_incomplete_input(self):
        incomplete_question = {"question": "what is your favorite city", "category": 2,"difficulty": 1}
        res = self.client().post('/questions', json=incomplete_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")

    def test_post_question_on_wrong_endpoint(self):
        res = self.client().post('/questions/15', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method not allowed")

    def test_search_questions_with_results(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'title'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], 2)

    def test_search_questions_without_results(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'bizarre'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # test quiz
    def test_quiz(self):
        mysearch = {"previous_questions": [], "quiz_category": {'type': 'Art', 'id': '6'}}
        res = self.client().post('/quizzes', json=mysearch)
        data = json.loads(res.data)
        print(f"quiz question id: {data}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_quiz_incomplete_input(self):
        mysearch = {"quiz_category": {'type': 'Art', 'id': '6'}}
        res = self.client().post('/quizzes', json=mysearch)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

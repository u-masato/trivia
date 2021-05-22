import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            "answer": "Scarab",
            "category": 1,
            "difficulty": 4,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        }

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
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('categories'))

    def test_get_questions(self):
        res = self.client().get('/questions?page=1')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('questions'))

    def test_get_questions_not_found(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data.get('success'), False)

    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('question'))

    def test_get_questions_unprocessable(self):
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data.get('success'), False)

    def test_delete_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        question_id = data.get('question').get('id', 1)
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)

    def test_delete_question_not_found(self):
        res = self.client().delete('/questions/9999')

        self.assertEqual(res.status_code, 404)

    def test_search_by_question(self):
        res = self.client().post('/questions/search', json={'searchTerm': ''})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('questions'))

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('questions'))
        self.assertTrue(data.get('total_questions'))
        self.assertTrue(data.get('current_category'))
        self.assertTrue(data.get('categories'))

    def test_get_questions_by_category_not_found(self):
        res = self.client().get('/categories/100/questions')

        self.assertEqual(res.status_code, 404)

    def test_play_quiz(self):
        json_data = {'previous_questions': [],
                     'quiz_category': {
                         'id': 1,
                         'type': 'Science'
                     }}
        res = self.client().post('quizzes', json=json_data)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('question'))

        json_data = {'previous_questions': [],
                     'quiz_category': {
                         'id': 0,
                         'type': 'click'
                     }}
        res = self.client().post('quizzes', json=json_data)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('question'))

    def test_play_quiz_not_found(self):
        json_data = {'previous_questions': [],
                     'quiz_category': {
                         'id': 99,
                         'type': 'Science'
                     }}
        res = self.client().post('quizzes', json=json_data)
        self.assertEqual(res.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

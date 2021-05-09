import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def get_pagenation(request, selections):
    page = request.args.get('page', 1, type=int)

    current_questions = [q.format() for q in selections]
    start = QUESTIONS_PER_PAGE * (page - 1)
    end = start + QUESTIONS_PER_PAGE
    return current_questions[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={r"*": {"origins": "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS')
        return response

    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''

    @app.route('/categories/', methods=['GET'])
    def get_categories():
        categories = [category.type for category in Category.query.all()]

        return jsonify({
            'categories': categories
        })

    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 
  
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    @app.route('/questions', methods=['GET'])
    def get_questions():
        # 10 questions
        questions = Question.query.all()
        selections = get_pagenation(request, questions)
        categories = [category.type for category in Category.query.all()]
        return jsonify({
            'questions': selections,
            'total_questions': len(Question.query.all()),
            'current_category': None,
            'categories': categories
        })

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
  
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter_by(id=question_id).one_or_none()
        if not question:
            abort(404)
        try:
            question.delete()
        except:
            abort(500)
        finally:
            db.session.close()

        return jsonify({
            'success': True
        })

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
  
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        question = body.get('question')
        answer = body.get('answer')
        category = body.get('category')
        difficulty = body.get('difficulty')

        # bad parameter
        if not all([question, answer, category, difficulty]):
            abort(422)

        question = Question(
            question=question,
            answer=answer,
            category=category + 1,
            difficulty=difficulty
        )
        try:
            question.insert()
        except:
            abort(500)

        return jsonify({
            'question': question.format()
        })

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
  
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', '')
        questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        selections = get_pagenation(request, questions)
        categories = [category.type for category in Category.query.all()]
        return jsonify({
            'questions': selections,
            'total_questions': len(Question.query.all()),
            'current_category': None,
            'categories': categories
        })

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        # offset category_id
        category_id += 1
        questions = Question.query.filter_by(category=category_id).all()
        if not questions:
            abort(404)

        selections = get_pagenation(request, questions)
        categories = [category.type for category in Category.query.all()]
        return jsonify({
            'questions': selections,
            'total_questions': len(Question.query.all()),
            'current_category': Category.query.get(category_id).format(),
            'categories': categories
        })

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
  
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    @app.route('/quizzes', methods=['GET', 'POST'])
    def play_quiz():
        body = request.get_json()
        print(body)
        previous_questions = body.get('previous_questions')
        quiz_category_id = body.get('quiz_category').get('id', 0)
        category = body.get('quiz_category').get('type')

        # case ALL
        if category == 'click':
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(category=quiz_category_id).all()

        if not questions:
            abort(404)

        question = None
        number = start_number = random.randint(0, len(questions) - 1)
        while True:
            if questions[number].id not in previous_questions:
                question = questions[number]
                break
            number += 1
            if number >= len(questions):
                number = 0
            if number == start_number:
                break

        return jsonify({
            'question': question.format() if question else None,
        })

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
    @app.errorhandler(404)
    def not_found(error):
        print(error)
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        print(error)
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable entity"
        }), 422

    return app


if __name__ == '__main__':
    app = create_app(test_config=True)
    app.run(debug=True)

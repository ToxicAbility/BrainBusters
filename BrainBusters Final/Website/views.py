import random
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Questions, Variants
from . import db
from sqlalchemy.sql.expression import func
from flask import jsonify

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def homepage():
    top_players = User.query.order_by(User.points.desc()).limit(5).all()
    return render_template('Homepage.html', top_players=top_players)

def retrieve_questions_from_database():
    questions = Questions.query.all()  # This gets all question objects from the database
    return questions


@views.route('/game', methods=['GET', 'POST'])
def game():
    # Assume 'all_questions' retrieves all questions from the database
    all_questions = Questions.query.all()
    random.shuffle(all_questions)  # Shuffle the list to get random order
    questions = all_questions[:6]  # Select first 6 questions for 6 blocks

    return render_template('QuestionsPage.html', questions=questions)

@views.route('/answer', methods=['POST', 'GET'])
@login_required
def answer():
    question_id = request.form.get('question_id')
    user_answer = request.form.get(f'answer_{question_id}')

    if not question_id or not user_answer:
        flash('Invalid submission', 'error')
        return redirect(url_for('views.game'))

    question = Questions.query.get(question_id)
    if not question:
        flash('Question does not exist.', 'error')
        return redirect(url_for('views.game'))

    if question.answer.lower() == user_answer.lower():
        current_user.points += 1
        db.session.commit()
        flash('Correct answer!', 'success')
    else:
        # Logic to remove the question or indicate that it's been answered incorrectly
        flash('Wrong answer!', 'error')
    
    return jsonify({'success': True})



@views.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if 'reset_leaderboard' in request.form:
            # Reset logic here
            User.query.update({User.points: 0})
            db.session.commit()
            flash('Leaderboard has been reset successfully.', 'success')
            return redirect(url_for('views.admin'))
        else:
            # Your existing code for adding a question
            question_text = request.form.get('question')
            answer_text = request.form.get('answer')
            variants = [request.form.get('variant1'), request.form.get('variant2'), answer_text]

            question = Questions(question=question_text, answer=answer_text)
            db.session.add(question)
            db.session.commit()

            for variant in variants:
                new_variant = Variants(question_id=question.id, variants=variant)
                db.session.add(new_variant)
            db.session.commit()
            flash('New question and variants added successfully.', 'success')
            
    return render_template('AdminPanel.html')

  
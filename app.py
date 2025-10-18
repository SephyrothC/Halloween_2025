from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Chemins vers les fichiers JSON
QUESTIONS_FILE = 'data/questions.json'
SCORES_FILE = 'data/scores.json'

# Charger les questions
def load_questions():
    if os.path.exists(QUESTIONS_FILE):
        try:
            with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            print(f"Erreur lors du chargement des questions: {e}")
            return {}
    return {}

# Charger les scores
def load_scores():
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            print(f"Erreur lors du chargement des scores: {e}")
            # Recréer le fichier s'il est corrompu
            save_scores([])
            return []
    return []

# Sauvegarder les scores
def save_scores(scores):
    with open(SCORES_FILE, 'w', encoding='utf-8') as f:
        json.dump(scores, f, indent=2, ensure_ascii=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz/<question_uuid>')
def quiz(question_uuid):
    questions = load_questions()
    if question_uuid not in questions:
        return "Question introuvable!", 404
    question_data = questions[question_uuid]
    # Vérifier si la question a déjà été répondue
    answered = session.get('answered_questions', [])
    already_answered = question_uuid in answered
    return render_template('quiz.html', 
                         question_id=question_uuid,
                         question=question_data['question'],
                         choices=question_data['choices'],
                         already_answered=already_answered)

@app.route('/submit', methods=['POST'])
def submit_answer():
    data = request.json
    question_id = data.get('question_id')  # UUID string
    answer = data.get('answer')
    player_name = data.get('player_name', 'Anonyme')

    questions = load_questions()
    if question_id not in questions:
        return jsonify({'success': False, 'message': 'Question introuvable'})

    # Vérifier si la question a déjà été répondue
    if 'answered_questions' not in session:
        session['answered_questions'] = []

    if question_id in session['answered_questions']:
        return jsonify({
            'success': False,
            'message': 'Vous avez déjà répondu à cette question!',
            'correct': False
        })

    correct_answer = questions[question_id]['correct']
    is_correct = (answer == correct_answer)

    # Marquer la question comme répondue
    session['answered_questions'].append(question_id)
    session.modified = True

    # Si la réponse est correcte, ajouter un point
    if is_correct:
        scores = load_scores()
        # Chercher si le joueur existe déjà
        player_found = False
        for player in scores:
            if player['name'].lower() == player_name.lower():
                player['score'] += 1
                player['last_updated'] = datetime.now().isoformat()
                player_found = True
                break
        # Si le joueur n'existe pas, le créer
        if not player_found:
            scores.append({
                'name': player_name,
                'score': 1,
                'last_updated': datetime.now().isoformat()
            })
        # Trier par score décroissant
        scores.sort(key=lambda x: x['score'], reverse=True)
        save_scores(scores)

    return jsonify({
        'success': True,
        'correct': is_correct,
        'message': 'Bonne réponse! +1 point 🎃' if is_correct else f'Mauvaise réponse! La bonne réponse était: {correct_answer}'
    })

@app.route('/leaderboard')
def leaderboard():
    scores = load_scores()
    return render_template('leaderboard.html', scores=scores)

@app.route('/api/leaderboard')
def api_leaderboard():
    scores = load_scores()
    return jsonify(scores)

@app.route('/reset')
def reset():
    """Route pour réinitialiser la session (pour tester)"""
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Créer les fichiers de données s'ils n'existent pas
    if not os.path.exists('data'):
        os.makedirs('data')
    
    if not os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f)
    
    if not os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
    
    # Lancer le serveur sur toutes les interfaces (important pour Docker)
    app.run(host='0.0.0.0', port=5000, debug=True)

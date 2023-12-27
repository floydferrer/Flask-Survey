from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = -1
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
# responses = []

questions = {}
for q in satisfaction_survey.questions:
    questions[satisfaction_survey.questions.index(q)] = q.question

choices = {}
for c in satisfaction_survey.questions:
    choices[satisfaction_survey.questions.index(c)] = c.choices

@app.route('/survey')
def show_survey():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('survey.html', title=title, instructions=instructions)

@app.route('/reset', methods=['POST'])
def reset_responses():
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/questions/<q>')
def show_question(q):
    while int(q) < len(session['responses']):
        responses = session['responses']
        responses.pop()
        session['responses'] = responses
    if (len(session['responses']) < int(q)):
        flash('Please complete current question!')
        return redirect(f'/questions/{len(session["responses"])}')
    qtn = questions[int(q)]
    return render_template(f'questions/{q}.html', q=int(q)+1, qtn=qtn, choices=choices)

@app.route('/answer/<q>', methods=['POST'])
def add_response(q):
    responses = session['responses']
    responses.append(request.form.get('answer'))
    session['responses'] = responses
    return redirect(f'/questions/{q}')

@app.route('/thank-you', methods=['POST'])
def view_responses():
    responses = session['responses']
    responses.append(request.form.get('answer'))
    session['responses'] = responses
    return render_template('thank-you.html', results=responses)
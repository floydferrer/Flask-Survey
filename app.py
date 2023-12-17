from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = -1
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
responses = []

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

@app.route('/questions/<q>')
def show_question(q):
    while int(q) < len(responses):
        responses.pop()
    if (len(responses) < int(q)):
        flash('Please complete current question!')
        return redirect(f'/questions/{len(responses)}')
    qtn = questions[int(q)]
    return render_template(f'questions/{q}.html', q=int(q)+1, qtn=qtn, choices=choices)

@app.route('/answer/<q>', methods=['POST'])
def add_response(q):
    responses.append(request.form.get('answer'))
    return redirect(f'/questions/{q}')

@app.route('/thank-you', methods=['POST'])
def view_responses():
    responses.append(request.form.get('answer'))
    return render_template('thank-you.html', results=responses)
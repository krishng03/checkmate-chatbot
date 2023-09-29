import subprocess
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/dtl'
db = SQLAlchemy(app)
app.secret_key = 'super-secret-key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
app.config['SESSION_COOKIE_SECURE'] = True

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Stories(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class ChatConversation(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    prompt = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    if 'user' in session:
        uid = session['user']
        username = User.query.get(uid)
        return render_template('index.html', btn='Logout', name=username.name)
    return render_template('index.html')

@app.route('/chatbot')
def chatbot():
    user_id = session['user']
    username = User.query.get(user_id).name
    conversations = ChatConversation.query.filter_by(user_id=user_id).order_by(ChatConversation.timestamp.asc()).all()
    return render_template('chatbot.html', name=username, conversations=conversations)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/share', methods=['GET', 'POST'])
def share():
    if request.method == 'POST':
        story_text = request.form.get('story')
        if story_text:
            username = (User.query.get(session['user'])).name
            new_story = Stories(name=username, message=story_text)
            db.session.add(new_story)
            db.session.commit()
    stories = Stories.query.order_by(Stories.id.desc()).all()
    return render_template('share.html', stories=stories)

@app.route('/login', methods=['POST', 'GET'])
def login():
    alert_message = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                session['user'] = user.id 
                return render_template('index.html', btn='Logout', name=user.name)
            else:
                alert_message = 'Invalid Password, Try Again!'
        else:
            alert_message = 'Invalid Credentials, Try Again!'
    return render_template('login.html', alert_message=alert_message)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        if user:
            session['user'] = user.id
            return render_template('index.html', btn='Logout', name=user.name)
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/login')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_prompt = request.json.get('user_prompt', '')
    user_id = session.get('user')
    username = User.query.get(user_id).name
    try:
        response = subprocess.check_output(['python', 'main.py', user_prompt, username], text=True)
        conversation = ChatConversation(user_id=user_id, prompt=user_prompt, answer=response)
        db.session.add(conversation)
        db.session.commit()
    except subprocess.CalledProcessError:
        response = "An error occurred while processing the request."
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
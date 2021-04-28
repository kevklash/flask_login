from flask import (
    Flask,
    g,
    abort,
    redirect,
    render_template,
    request,
    session,
    url_for
)


""" g is like a global variable or store that is available across the request context """


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

        def __repr__(self):
            return f'<User: {self.username}>'


users = []
users.append(User(id=1, username='Kevin', password='password'))
users.append(User(id=2, username='Alberto', password='password'))
users.append(User(id=3, username='Fatimita', password='password'))
users.append(User(id=4, username='Diny', password='password'))
users.append(User(id=5, username='Carlos', password='password'))
""" print(users) """


app = Flask(__name__)
""" Setting secret key as it is required for sessions """
app.secret_key = 'somesecretkeythatonlyishouldknow'


""" Checking if the user id exists in the session """
@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        """ Removing a session if logged in, when trying to log in again """
        session.pop('user_id', None)
        username = request.form['username']
        password= request.form['password']

        user = [x for x in users if x.username == username][0]
        if user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))
        
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/profile')
def profile(): 
    """ If there is no session """
    if not g.user:
        return redirect(url_for('login'))
        """ Or abort(403) """

    return render_template('profile.html')
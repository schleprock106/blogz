from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner_id = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'display_user', 'display_blogs']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash('Logged in')
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():


    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify']
        username_error = ""
        password_error = ""
        verify_password_error = ""
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            username_error = "Username alreasy exist, please enter another username."


        if len(username) < 3 or len(username) > 20:
            username_error = "Please enter valid username, (3-20) characters."

        if len(password) < 3 or len(password) > 20:
            password_error = "Please enter valid password, (3-20) characters"

        if verify_password != password:
            verify_password_error = "Passwords do not match. Please re-enter password"


        if len(username_error) !=0 or len(password_error) !=0 or len(verify_password_error) != 0:
            return render_template("signup.html", username_error = username_error, password_error = password_error,
            verify_password_error = verify_password_error)
            
        else:  
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')

    return render_template('signup.html')
       
         

    

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')
    

@app.route('/', methods = ['POST', 'GET'])
def display_user():
    users = User.query.all()
    return render_template('index.html', users = users)
  


@app.route('/blogs')
def display_blogs():

    
    if request.args.get('id'):       
        
        blog_id = request.args.get('id')
        blog = Blog.query.get(blog_id)
        return render_template('individual.html', blog = blog)
       
    elif request.args.get('user'):
        user_id = request.args.get('user')
        user = User.query.get(user_id)
        blogs = Blog.query.filter_by(owner_id = user_id).all()
        return render_template('singleUser.html', blogs = blogs)
    else:
        blogs = Blog.query.all()
        return render_template('blogs.html', blogs = blogs, title = 'All Blogs')
        




@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
    
        title_error = ''
        body_error = ''
        
        title = request.form['title']
        body = request.form['body']

        owner = User.query.filter_by(username=session['username']).first()

        if title == '':
            title_error = "Please enter Blog Title"

        if body == '':
            body_error = "Please enter text for blog"

        if not title_error and not body_error:

            blog = Blog(title, body, owner)
            
            db.session.add(blog)
            db.session.commit()


            return redirect ('/individual?id=' + str(blog.id))

    else:
        return render_template ('new_post.html')    


    
@app.route('/individual', methods =  ['GET'])
def individual_post():


    blog_id = request.args.get('id')
    blog = Blog.query.filter_by(id=blog_id).first()
    title = blog.title
    body = blog.body
    author = blog.owner

    return render_template('individual.html', title = title, body = body, author = author)



    

if __name__ == "__main__":        
    app.run()   
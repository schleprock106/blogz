from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'



class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))

    def __init__(self, title, body):
        self.title = blog_title
        self.body = blog_body


@app.route('/', methods = ['POST','GET'])
def display_blogs():

    blogs = Blog.query.all()

    return render_template('blogs.html', title="Build-a Blog", blogs = blogs)



@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    blog_title = ''
    blog_body = ''

    

    title_error = ''
    body_error = ''

    if request.method == 'POST':
        
        title = request.form['blog_title']
        body = request.form['blog_body']

        if blog_title == '':
            title_error = "Please enter Blog Title"

        if blog_body == '':
            body_error = "Please enter text for blog"

        if title_error and body_error:
            return render_template('new_post.html', title_error = title_error, body_error = body_error)
        elif title_error  and not body_error:
            return render_template('new_post.html', blog_body, title_error = title_error)
        elif body_error  and not title_error:
            return render_template('new_post.html', blog_title, body_error = body_error)

    

    else:
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()

        return redirect ('/')

    if request.method == 'GET':
        return render_template ('new.post.html')
    

if __name__ == "__main__":        
    app.run()   
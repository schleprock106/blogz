from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
# app.config['SQLALCHEMY_ECHO'] = True
# db = SQLAlchemy(app)
# app.secret_key = 'y337kGcys&zP3B'

blogs = []

# class Blog(db.Model):

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(120))
#     body = db.Column(db.String(300))

#     def __init__(self, title, body):
#         self.title = title
#         self.body = body


@app.route('/blog')
def display_blogs():

    return render_template('blogs.html', title="Build-a Blog", blogs=blogs)



@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blogs.append(blog_title)
        return redirect('/blog')
        
    return render_template('new_post.html')
    


app.run()   
from flask import Flask, request, redirect, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

blogs = []


@app.route('/blog', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog = request.form['blog']
        blog.append(blog)


    return render_template('blogs.html', title="Build-a-Blog", blog=blog)

app.run()
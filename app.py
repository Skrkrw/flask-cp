from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Comment for myself: Look for Jedi and  Python Language Server
# IntelliSense - VS IntelliCode
app = Flask(__name__)

# Telling flask where the database will be and we can use whatever DB we like
# /// = Relative Path to app.py
# //// = Absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
# Creating the DB and linking with app.py 
db = SQLAlchemy(app)

app.config['SERVER_NAME'] = 'localhost:5000'

# Each class variable is consider as a pice or data on the DB
# The first thing almost all model should have is an 'id'
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # __repr__ should return a printable representation of the object
    def __repr__(self):
    # __repr__ is more for developers while __str__ is for end users.
        return 'Blog post ' + str(self.id)

"""
Dommie Data
all_posts = [
    {
        'title': 'Post 1',
        'comment': 'Comment 1 for this post',
        'author': 'Jose'
    },
    {
        'title': 'Post 2',
        'comment': 'Comment 2 for this post',
    }
]
"""


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts/', methods=['GET', 'POST']) # Allowing Get and Post
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        # We dont define date time because it is automatically, or default
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        # Creating a new entry in the DB
        db.session.add(new_post)
        # Only after commiting the new entry it will be in the DB
        # It will create a permanent entry and not just the current session
        # While the server still running
        db.session.commit()
        return redirect('/posts/')
    else:
        # Getting all of the BLogPost from DB
        all_posts = BlogPost.query.order_by(BlogPost.date_created).all()
        return render_template('posts.html', posts=all_posts)

"""
@app.route('/home/user/<string:name>/id/<int:id>')
def hello(name, id):
    return "Hello, " + name + " your ID is: " + str(id)


# methods=['GET'] or ['POST'] or ['GET', 'POST']
@app.route('/only_get', methods=['GET'])
def get_req():
    return 'You can only get this webpage!'
"""


@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts/')


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/posts/')
    else:
        return render_template('edit.html', post=post)

@app.route('/posts/new/', methods=["GET", "POST"])
def new_post():

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()

        return redirect('/posts/')
    else:
        return render_template('new_post.html')


if __name__ == "__main__":
    # Enables developer mode
    # Throwing an error messages and not a 404
    app.run(debug=True)
    # Also allows to update the server on the flypython
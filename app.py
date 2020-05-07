from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def posts():
    return render_template('posts.html')

@app.route('/home/user/<string:name>/id/<int:id>')
def hello(name, id):
    return "Hellor, " + name + " your ID is: " + str(id)


# methods=['GET'] or ['POST'] or ['GET', 'POST']
@app.route('/only_get', methods=['GET'])
def get_req():
    return 'You can only get this webpage!'





if __name__ == "__main__":
    # Enables developer mode
    # Throwing an error messages and not a 404
    app.run(debug=True)
    # Also allows to update the server on the flypython
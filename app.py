from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)


class Todo(db.Model):  # here we are defining the schema of our database
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    des = db.Column(db.String(600), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:  # what ever we wantb to be seen we can add in it's return
        return f"{self.sno} - {self.title}"


# with app.app_context():
#     db.create_all()


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        des = request.form['des']
        todo = Todo(title=title, des=des)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)


@app.route('/show')  # this will print all the data base stored in our todo.db in the mentioned repr format
def show():
    allTodo = Todo.query.all()
    print(allTodo)
    return "done"


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        des = request.form['des']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.des = des
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)


@app.route('/delete/<int:sno>')  # here we are mentioning the delete type, as we will delete the s.no which would delete the content in that s.no
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=False, port=8000)

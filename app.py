from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    date = db.Column(db.Date)


def _arrange_items(todo_list):
    items = filter(lambda todo: not todo.complete and todo.date, todo_list)
    result = sorted(items, key=lambda x: x.date)

    items = filter(lambda todo: not todo.complete and not todo.date, todo_list)
    result += sorted(items, key=lambda todo: todo.title)

    items = filter(lambda todo: todo.complete and todo.date, todo_list)
    result += sorted(items, key=lambda x: x.date)

    items = filter(lambda todo: todo.complete and not todo.date, todo_list)
    result += sorted(items, key=lambda todo: todo.title)

    return result


@app.route("/")
def index():
    todo_list = _arrange_items(Todo.query.all())
    return render_template(
        "base.html", todo_list=todo_list, today=datetime.date(datetime.now())
    )


@app.route("/add", methods=["POST"])
def add():
    try:
        date = datetime.fromisoformat(request.form.get("todo_date"))
    except:
        date = None

    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False, date=date)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


# if __name__ == '__main__':
#     # db.create_all()

#     # new_todo = Todo(title="todo alicate", complete=False)
#     # db.session.add(new_todo)
#     # db.session.commit()
#     ...

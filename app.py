from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dateutil.relativedelta import *
from dataclasses import dataclass

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    date = db.Column(db.Date)


@dataclass
class IndexTodoItem:
    id: int
    title: str
    complete: bool
    date: datetime

    def __post_init__(self):
        if not self.date:
            return

        relative = relativedelta(self.date, datetime.now())
        inteval, period = self._get_interval(relative)
        message = self._get_message(relative, inteval)
        self.message = message.format(inteval, period)

    def _get_interval(self, relative: relativedelta):
        if relative.years != 0:
            interval = abs(relative.years)
            message_interval = "ano{}".format("s" if interval != 1 else "")
            return (interval, message_interval)

        if relative.months != 0:
            interval = abs(relative.months)
            message_interval = "mes{}".format("es" if interval != 1 else "")
            return (interval, message_interval)

        interval = abs(relative.days)
        message_interval = "dia{}".format("s" if interval != 1 else "")
        return (interval, message_interval)

    def _get_message(self, relative: relativedelta, interval):
        if relative.years == 0 and relative.months == 0 and relative.days == 0:
            if relative.hours <= 0 or relative.minutes <= 0 or relative.seconds <= 0:
                return "A tarefa vence hoje"
            else:
                return "A tarefa vence amanhã"

        if relative.years < 0 or relative.months < 0 or relative.days < 0:
            return "A tarefa está atrasada há {} {}"

        return (
            "Falta{}".format("m" if interval > 1 else "")
            + " {} {} para a conclusão da tarefa"
        )


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
    todo_list = [
        IndexTodoItem(item.id, item.title, item.complete, item.date)
        for item in todo_list
    ]

    return render_template(
        "base.html", todo_list=todo_list, today=datetime.date(datetime.now()),
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

from flask import Flask, render_template, request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno}-{self.name}"
    

@app.route("/",methods=['GET','POST'])
def todo_app():
    if request.method=='POST':
        name=request.form['name']
        desc=request.form['desc']
        todo=Todo(name=name,desc=desc)
        db.session.add(todo)
        db.session.commit()

    alltodo=Todo.query.all()
    # print(alltodo)
    return render_template('index.html',alltodo=alltodo)

@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
            name=request.form['name']
            desc=request.form['desc']
            task=Todo.query.filter_by(sno=sno).first()
            task.name=name
            task.desc=desc
            db.session.add(task)
            db.session.commit()   
            return redirect("/tasks")
    task=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=task)

@app.route("/delete/<int:sno>")
def delete(sno):
    task=Todo.query.filter_by(sno=sno).first()
    db.session.delete(task)
    db.session.commit()
    return redirect("/tasks")

@app.route("/home")
def home():
    return redirect("/")

@app.route("/create")
def create():
    return render_template('create.html')

@app.route("/tasks")
def tasks():
    alltodo=Todo.query.all()
    return render_template('tasks.html',alltodo=alltodo)

if __name__ == '__main__':
   app.run(debug=False)
from flask import Flask,abort,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///project.db"
db=SQLAlchemy(app)


class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    task=db.Column(db.String,nullable=False)
    desc=db.Column(db.String,nullable=False)
    time=db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc))
    def __repr__(self):
        return f"{self.sno} - {self.task}"

with app.app_context():
    db.create_all()

@app.route('/',methods=['GET','POST'])
def adding_data():
    if request.method=="POST":
        todo=Todo(
            task=request.form['title'],
            desc=request.form['description']
        )
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template("base.html", alltodo=alltodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    alltodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(alltodo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    alltodo = Todo.query.filter_by(sno=sno).first()
    if alltodo is None:
        abort(404)
    if request.method == 'POST':
        alltodo.task = request.form['title']
        alltodo.desc = request.form['description']
        db.session.commit()
        return redirect('/')
    return render_template("update.html", alltodo=alltodo)
if __name__ == '__main__':

    app.run(debug=True)
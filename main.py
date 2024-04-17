from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'


# Form for adding new books
class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired()])
    submit = SubmitField('Add Book')


# Route to show all books
@app.route('/', methods=['GET', 'POST'])
def home():
    books = Book.query.all()
    return render_template('index.html', books=books)


# Route to add new books
@app.route("/add", methods=['GET', 'POST'])
def add():
    form = BookForm()
    if form.validate_on_submit():
        new_book = Book(title=form.title.data, author=form.author.data, rating=form.rating.data)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)


# Route to edit a book's rating
@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        book.rating = form.rating.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', form=form)


# Route to delete a book
@app.route('/delete/<int:book_id>', methods=['GET', 'POST'])
def delete(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))


# Initialize the database
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

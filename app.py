from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Book Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100))
    pages = db.Column(db.Integer)
    completed = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Integer)  # 1-5 stars
    started_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    books = Book.query.order_by(Book.started_at.desc()).all()
    return render_template('index.html', books=books)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    author = request.form.get('author')
    pages = request.form.get('pages')
    
    if title and author:  # Basic validation
        new_book = Book(
            title=title,
            author=author,
            pages=int(pages) if pages else None
        )
        db.session.add(new_book)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/toggle/<int:book_id>')
def toggle(book_id):
    book = Book.query.get_or_404(book_id)
    book.completed = not book.completed
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/rate/<int:book_id>/<int:rating>')
def rate(book_id, rating):
    book = Book.query.get_or_404(book_id)
    book.rating = rating
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:book_id>')
def delete(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
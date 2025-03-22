from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Movie Model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year_aired = db.Column(db.Integer)
    watched = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Integer, default=1)  # 1-5 stars

    def __repr__(self):
        return f'<Movie {self.title}>'

# Create database tables
with app.app_context():
    db.create_all()

#For home page
@app.route('/')
def index():
    movies = Movie.query.order_by(Movie.title.desc()).all()
    range_values = range(1, 6) # Ratings from 1 to 5 stars
    return render_template('index.html', movies=movies, range_values=range_values)

#Adds movies to DB
@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    year_aired = request.form.get('year_aired')
    rating = request.form.get('rating')
    
    if title and year_aired and rating:  # Basic validation
        new_movie = Movie(
            title=title,
            year_aired=int(year_aired),
            rating=int(rating)
        )
        db.session.add(new_movie)
        db.session.commit()
    return redirect(url_for('index'))

#Updates whether watched or not watched
@app.route('/toggle/<int:movie_id>')
def toggle(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    movie.watched = not movie.watched
    db.session.commit()
    return redirect(url_for('index'))

#Updates rating
@app.route('/rate/<int:movie_id>/<int:rating>')
def rate(movie_id, rating):
    movie = Movie.query.get_or_404(movie_id)
    movie.rating = rating
    db.session.commit()
    return redirect(url_for('index'))

#Deletes movie from list
@app.route('/delete/<int:movie_id>')
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
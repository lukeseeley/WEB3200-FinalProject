from flask import Flask, render_template, url_for, request, redirect, abort
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import click


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}{}'.format(app.root_path, 'media.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'b2de7FkqvkMyqzNFzxCkgnPKIGP6i4Rc'

db = SQLAlchemy(app)

class Employee(db.Model):
    employeeId = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    jobtitle = db.Column(db.String(100), nullable=False)

class Game(db.Model):
    gameId = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    publisher = db.Column(db.String(100), nullable = True)
    developer = db.Column(db.String(100), nullable = True)
    description = db.Column(db.Text, nullable = False)

class Movie(db.Model):
    movieId = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    director = db.Column(db.String(100), nullable = True)
    actors = db.Column(db.Text, nullable = False)
    description = db.Column(db.Text, nullable = False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def check_password(self, value):
        return check_password_hash(self.password, value)

db.create_all()

from admin import admin_blueprint

@click.command("add-content")
@with_appcontext
def add_content():
    objects = [ 
            Employee(firstname = "John", lastname = "Wick", jobtitle = "Hitman"),
            Employee(firstname = "Sarah", lastname = "Connor", jobtitle = "Time Traveler"),
            Employee(firstname = "Rock", lastname = "Johnson", jobtitle = "Video Game Character"),
            Employee(firstname = "Rachel", lastname = "Amber", jobtitle = "Aspiring Actor"),
            Game(title = "Fallout 4", publisher = "Bethesda Softworks", developer = "Bethesda Game Studios", description = "Bethesda Game Studios, the award-winning creators of Fallout 3 and The Elder Scrolls V: Skyrim, welcome you to the world of Fallout 4 – their most ambitious game ever, and the next generation of open-world gaming."),
            Game(title = "Terraria", publisher = "Re-Logic", developer = "Re-Logic", description = "Dig, fight, explore, build! Nothing is impossible in this action-packed adventure game. Four Pack also available!"),
            Game(title = "Factorio", publisher = "Wube Software LTD.", developer = "Wube Software LTD.", description = "Factorio is a game about building and creating automated factories to produce items of increasing complexity, within an infinite 2D world. Use your imagination to design your factory, combine simple elements into ingenious structures, and finally protect it from the creatures who don't really like you."),
            Game(title = "Stellaris", publisher = "Paradox Interactive", developer = "Paradox Development Studio", description = "Explore a galaxy full of wonders in this sci-fi grand strategy game from Paradox Development Studios. Interact with diverse alien races, discover strange new worlds with unexpected events and expand the reach of your empire. Each new adventure holds almost limitless possibilities."),
            Game(title = "Borderlands 2", publisher = "2K", developer = "Gearbox Software", description = "A new era of shoot and loot is about to begin. Play as one of four new vault hunters facing off against a massive new world of creatures, psychos and the evil mastermind, Handsome Jack. Make new friends, arm them with a bazillion weapons and fight alongside them in 4 player co-op on a relentless quest for revenge and redemption across the undiscovered and unpredictable living planet."),
            Game(title = "Portal 2", publisher = "Valve", developer = "Valve", description = "Portal 2 draws from the award-winning formula of innovative gameplay, story, and music that earned the original Portal over 70 industry accolades and created a cult following."),
            Movie(title = "The Lord of the Rings: The Return of the King", director = "Peter Jackson", actors = "Elijah Wood, Viggo Mortensen, Ian McKellen", description = "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring. "),
            Movie(title = "Forrest Gump", director = "Robert Zemeckis", actors = "Tom Hanks, Robin Wright, Gary Sinise", description = "The presidencies of Kennedy and Johnson, the events of Vietnam, Watergate and other historical events unfold through the perspective of an Alabama man with an IQ of 75, whose only desire is to be reunited with his childhood sweetheart. "),
            Movie(title = "Inception", director = "Christopher Nolan", actors = "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page", description = "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O. "),
            Movie(title = "Star Wars: Episode V - The Empire Strikes Back", director = "Irvin Kershner", actors = "Mark Hamill, Harrison Ford, Carrie Fisher", description = "After the Rebels are brutally overpowered by the Empire on the ice planet Hoth, Luke Skywalker begins Jedi training with Yoda, while his friends are pursued by Darth Vader and a bounty hunter named Boba Fett all over the galaxy. "),
            Movie(title = "The Matrix", director = "Lana Wachowski, Lilly Wachowski", actors = "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss", description = "When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence. "),
            User(username = "psdemo", password=generate_password_hash('psdemo')) 
        ]
    db.session.bulk_save_objects(objects)
    db.session.commit()

app.cli.add_command(add_content)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/games')
def viewgames():
    games = Game.query.all()
    return render_template('viewgames.html', games = games)

@app.route('/games/<gameId>')
def game(gameId):
    game = Game.query.filter(Game.gameId == gameId).first()
    return render_template('game.html', game = game)

@app.route('/movies')
def viewmovies():
    movies = Movie.query.all()
    return render_template('viewmovies.html', movies = movies)

@app.route('/movies/<movieId>')
def movie(movieId):
    movie = Movie.query.filter(Movie.movieId == movieId).first()
    return render_template('movie.html', movie = movie)

app.register_blueprint(admin_blueprint)
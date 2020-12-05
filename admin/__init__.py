from flask import Blueprint, render_template, url_for, request, redirect, abort, g, Blueprint
from datetime import datetime

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin', template_folder="templates")

from app import Employee, Game, Movie, User, db
from admin import auth


@admin_blueprint.route('/')
@auth.protected
def index():
    return render_template('admin/admin.html')


# =============== Employees ================== #
@admin_blueprint.route('/employees')
@auth.protected
def viewEmployees():
    employees = Employee.query.all()
    return render_template('admin/viewemployees.html', employees = employees)

@admin_blueprint.route('/employee/add', methods=('GET', 'POST'))
@auth.protected
def addEmployee():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        jobtitle = request.form['jobtitle']

        error = None

        if not firstname:
            error = "First Name is required"
        elif not lastname:
            error = "Last Name is required"
        elif not jobtitle:
            error = "Job Title is required"

        if error is None:
            employee = Employee(firstname = firstname, lastname = lastname, jobtitle = jobtitle)
            db.session.add(employee)
            db.session.commit()
            return redirect(url_for('admin.viewEmployees'))
    
    return render_template('admin/employee_form.html')

@admin_blueprint.route('employee/<employeeId>/edit', methods=('GET', 'POST'))
@auth.protected
def editEmployee(employeeId):
    employee = Employee.query.get_or_404(employeeId)

    if request.method == 'POST':
        employee.firstname = request.form['firstname']
        employee.lastname = request.form['lastname']
        employee.jobtitle = request.form['jobtitle']

        error = None

        if not request.form['firstname']:
            error = "First Name is required"
        elif not request.form['lastname']:
            error = "Last Name is required"
        elif not request.form['jobtitle']:
            error = "Job Title is required"

        if error is None:
            db.session.commit()
            return redirect(url_for('admin.viewEmployees'))

    return render_template('admin/employee_form.html', employee = employee)

@admin_blueprint.route('employee/<employeeId>/delete', methods=('GET', 'POST'))
@auth.protected
def deleteEmployee(employeeId):
    employee = Employee.query.get_or_404(employeeId)

    if request.method == 'POST':
        Employee.query.filter(Employee.employeeId == employeeId).delete()
        db.session.commit()
        return redirect(url_for('admin.viewEmployees'))

    return render_template('admin/delete_form.html', target = employee.firstname + " " + employee.lastname, listType = "Employee")
    

# =============== Games ================== #
@admin_blueprint.route('/games')
@auth.protected
def viewGames():
    games = Game.query.all()
    return render_template('admin/viewgames.html', games = games)

@admin_blueprint.route('/game/add', methods=('GET', 'POST'))
@auth.protected
def addGame():
    if request.method == 'POST':
        title = request.form['title']
        publisher = request.form['publisher']
        developer = request.form['developer']
        description = request.form['description']

        error = None

        if not title:
            error = "Title is required"
        elif not publisher:
            error = "Publisher is required"
        elif not developer:
            error = "Developer is required"
        elif not description:
            error = "Description is required"

        if error is None:
            game = Game(title = title, publisher = publisher, developer = developer, description = description)
            db.session.add(game)
            db.session.commit()
            return redirect(url_for('admin.viewGames'))
    
    return render_template('admin/game_form.html')

@admin_blueprint.route('game/<gameId>/edit', methods=('GET', 'POST'))
@auth.protected
def editGame(gameId):
    game = Game.query.get_or_404(gameId)

    if request.method == 'POST':
        game.title = request.form['title']
        game.publisher = request.form['publisher']
        game.developer = request.form['developer']
        game.description = request.form['description']

        error = None

        if not request.form['title']:
            error = "Title is required"
        elif not request.form['publisher']:
            error = "Publisher is required"
        elif not request.form['developer']:
            error = "Developer is required"
        elif not request.form['description']:
            error = "Description is required"

        if error is None:
            db.session.commit()
            return redirect(url_for('admin.viewGames'))

    return render_template('admin/game_form.html', game = game)

@admin_blueprint.route('game/<gameId>/delete', methods=('GET', 'POST'))
@auth.protected
def deleteGame(gameId):
    game = Game.query.get_or_404(gameId)
    
    if request.method == 'POST':
        Game.query.filter(Game.gameId == gameId).delete()
        db.session.commit()
        return redirect(url_for('admin.viewGames'))

    return render_template('admin/delete_form.html', target = game.title, listType = "Game")
    
# =============== Movies ================== # title, director, actors, description
@admin_blueprint.route('/movies')
@auth.protected
def viewMovies():
    movies = Movie.query.all()
    return render_template('admin/viewmovies.html', movies = movies)

@admin_blueprint.route('/movie/add', methods=('GET', 'POST'))
@auth.protected
def addMovie():
    if request.method == 'POST':
        title = request.form['title']
        director = request.form['director']
        actors = request.form['actors']
        description = request.form['description']

        error = None

        if not title:
            error = "Title is required"
        elif not director:
            error = "Director is required"
        elif not actors:
            error = "Actors are required"
        elif not description:
            error = "Description is required"

        if error is None:
            movie = Movie(title = title, director = director, actors = actors, description = description)
            db.session.add(movie)
            db.session.commit()
            return redirect(url_for('admin.viewMovies'))
    
    return render_template('admin/movie_form.html')

@admin_blueprint.route('movie/<movieId>/edit', methods=('GET', 'POST'))
@auth.protected
def editMovie(movieId):
    movie = Movie.query.get_or_404(movieId)

    if request.method == 'POST':
        movie.title = request.form['title']
        movie.director = request.form['director']
        movie.actors = request.form['actors']
        movie.description = request.form['description']

        error = None

        if not request.form['title']:
            error = "Title is required"
        elif not request.form['director']:
            error = "Director is required"
        elif not request.form['actors']:
            error = "Actors are required"
        elif not request.form['description']:
            error = "Description is required"

        if error is None:
            db.session.commit()
            return redirect(url_for('admin.viewMovies'))

    return render_template('admin/movie_form.html', movie = movie)

@admin_blueprint.route('movie/<movieId>/delete', methods=('GET', 'POST'))
@auth.protected
def deleteMovie(movieId):
    movie = Movie.query.get_or_404(movieId)
    
    if request.method == 'POST':
        Movie.query.filter(Movie.movieId == movieId).delete()
        db.session.commit()
        return redirect(url_for('admin.viewMovies'))

    return render_template('admin/delete_form.html', target = movie.title, listType = "Movie")
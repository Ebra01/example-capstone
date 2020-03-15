from flask import Blueprint, abort, flash, url_for, redirect, render_template, jsonify, request
from flaskr.models.models import Movies
from flaskr.auth.auth import requires_auth, AuthError
from .forms import MoviesForm
from datetime import datetime, timedelta

movie = Blueprint('movies', __name__)


# Useful functions
def get_availability(release_date):
    format = "%Y-%m-%d %H:%M"
    rd = datetime.strptime(release_date, format)

    availability = rd + timedelta(days=7)

    return availability


# JSON/Templates type routes
@movie.route('/movies')
#@requires_auth
def get_movies():
    movies = Movies.query.order_by(Movies.id).all()
    current = [m.display() for m in movies]

    content_type = request.headers.get('Content-Type')

    if content_type == 'application/json':

        if len(current) == 0:
            abort(404)

        return jsonify({
            'title': 'Movies Page',
            'body': current,
            'success': True
        })

    else:
        now = str(datetime.now())
        now = datetime.strptime(now[:19], '%Y-%m-%d %H:%M:%S')

        up_movies = []
        in_movies = []
        od_movies = []

        for items in current:
            release_date = items['release_date']

            if (now - release_date).days >= 7:
                od_movies.append(items)
            elif (release_date - now).days > 0:
                up_movies.append(items)
            else:
                in_movies.append(items)

        return render_template('pages/movies.html', title='Movies',
                               up_movies=up_movies, in_movies=in_movies, od_movies=od_movies)


@movie.route('/movies/<int:movie_id>')
#@requires_auth
def get_movie(movie_id):
    movie_ = Movies.query.filter(Movies.id == movie_id).first()

    if not movie_:
        abort(404)
    try:
        current = movie_.display()

        content_type = request.headers.get('Content-Type')

        if content_type == 'application/json':
            return jsonify({
                'title': f"Movie {current['title']}'s Page",
                'body': current,
                'success': True
            })
        else:
            return render_template('pages/movie.html', title=f'{current["title"]}', movie=current)
    except Exception as e:
        print(e)
        abort(422)


@movie.route('/movies', methods=['POST'])
#@requires_auth
def create_movies():
    body = request.get_json()

    if not body:
        abort(400)

    new_title = body.get('title')
    new_rd = body.get('release_date')

    if not new_title or not new_rd:
        abort(400)

    try:

        new_movie = Movies(title=new_title, release_data=new_rd,
                           availability=get_availability(new_rd))
        new_movie.insert()

        movies = Movies.query.order_by(Movies.id).all()
        current = [a.display() for a in movies]

        return jsonify({
            'title': 'Movies Page',
            'body': current,
            'success': True
        })
    except Exception as e:
        print(e)
        abort(422)


@movie.route('/movies/<int:movie_id>', methods=['DELETE', 'POST'])
#@requires_auth
def delete_movies(movie_id):
    movies = Movies.query.filter(Movies.id == movie_id).first()

    if not movies:
        abort(404)

    content_type = request.headers.get('Content-Type')

    try:
        movies.delete()

        if content_type == 'application/json':

            return jsonify({
                'title': 'Movies Page',
                'Deleted Movie': movie_id,
                'success': True
            })
        else:
            flash(f'Movie #{movie_id} was deleted successfully!', 'success')
    except Exception as e:
        print(e)
        if content_type == 'application/json':
            abort(422)
        else:
            flash(f'Cannot delete Movie #{movie_id} !', 'danger')
    return redirect(url_for('main.home'))


@movie.route('/movies/<int:movie_id>', methods=['PATCH'])
#@requires_auth
def update_movies(movie_id):
    movies = Movies.query.filter(Movies.id == movie_id).first()

    if not movies:
        abort(404)

    body = request.get_json()

    if not body:
        abort(400)

    updated_title = body.get('title')
    updated_rd = body.get('release_date')

    if not updated_title and not updated_rd:
        abort(400)

    try:
        if updated_title:
            movies.title = updated_title
        if updated_rd:
            movies.release_date = updated_rd

        movies.update()

        movies = Movies.query.order_by(Movies.id).all()
        current = [a.display() for a in movies]

        return jsonify({
            'title': 'Movies Page',
            'body': current,
            'success': True
        })

    except Exception as e:
        print(e)
        abort(422)


# Forms/Templates type routes
@movie.route("/movies/create", methods=['GET'])
#@requires_auth
def create_movies_form():
    form = MoviesForm()
    return render_template('forms/new_movie.html', form=form, title='New Movie')


@movie.route("/movies/create", methods=['POST'])
#@requires_auth
def create_movies_submission():
    form = MoviesForm()
    if form.validate_on_submit():

        availability = get_availability(request.form['release_date'])

        m = Movies(
            title=request.form['title'],
            release_data=request.form['release_date'],
            availability=availability
        )
        m.insert()
        flash(f'Movie {request.form["title"]} was successfully listed!', 'success')
        return redirect(url_for('movies.get_movies'))
    else:
        if 'title' in form.errors:
            error = 'Title must be a String'
        else:
            error = 'Release Date must be a DateTime(YYYY-MM-DD HH-MM) '
        flash(f'Unable to create a new movie ({error}) !', 'warning')

    return render_template('forms/new_movie.html', form=form, title='New Movie')


@movie.route('/movies/<int:movie_id>/edit', methods=['GET'])
#@requires_auth
def update_movies_form(movie_id):
    form = MoviesForm()

    movie_ = Movies.query.filter(Movies.id == movie_id).first()
    if not movie_:
        abort(404)

    try:
        current = movie_.display()
        form.title.data = current['title']
        form.release_date.data = current['release_date'].strftime('%Y-%m-%d %H:%M')

        return render_template('forms/edit_movie.html', form=form, movie=current, title=f'Edit - {current["title"]}')

    except Exception as e:
        print(e)
        abort(422)


@movie.route('/movies/<int:movie_id>/edit', methods=['POST'])
#@requires_auth
def update_movies_submission(movie_id):
    form = MoviesForm()

    movie_ = Movies.query.filter(Movies.id == movie_id).first()
    if not movie_:
        abort(404)

    current = movie_.display()

    try:
        if form.validate_on_submit():
            movie_.title = request.form['title']
            movie_.release_date = request.form['release_date']
            movie_.availability = get_availability(request.form['release_date'])
            movie_.update()

            flash(f'Movie {request.form["title"]} was successfully updated!', 'success')
            return redirect(url_for('movies.get_movie', movie_id=movie_id))
        else:
            flash(f'An error occurred. Movie {current["title"]} could not be updated!', 'warning')

        return render_template('forms/edit_movie.html', form=form, movie=current, title=f'Edit - {current["title"]}')
    except Exception as e:
        print(e)
        abort(422)

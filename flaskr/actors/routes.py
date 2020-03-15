from flask import Blueprint, abort, redirect, url_for, make_response, render_template, jsonify, request, flash
from flaskr.models.models import Actors
from flaskr.auth.auth import requires_auth, requires_scope, AuthError
from .forms import ActorsForm

actor = Blueprint('actors', __name__)


# JSON/Templates type routes
@actor.route('/actors')
#@requires_auth
def get_actors():
    actors_ = Actors.query.order_by(Actors.id).all()
    current = [a.display() for a in actors_]

    content_type = request.headers.get('Content-Type')

    if content_type == 'application/json':

        if len(current) == 0:
            abort(404)

        return jsonify({
            'title': 'Actors Page',
            'body': current,
            'success': True
        })

    else:
        actors = []
        actresses = []
        for items in current:
            if items['gender'] == 'male':
                actors.append(items)
            else:
                actresses.append(items)
        return render_template('pages/actors.html', title='Actors', actors=actors, actresses=actresses)


@actor.route('/actors/<int:actor_id>')
#@requires_auth
def get_actor(actor_id):
    actor_ = Actors.query.filter(Actors.id == actor_id).first()

    if not actor_:
        abort(404)
    try:
        current = actor_.display()

        content_type = request.headers.get('Content-Type')

        if content_type == 'application/json':
            return jsonify({
                'title': f"Actor {current['name']}'s Page",
                'body': current,
                'success': True
            })
        else:
            return render_template('pages/actor.html', title=f'{current["name"]}', actor=current)
    except Exception as e:
        print(e)
        abort(422)


@actor.route('/actors', methods=['POST'])
#@requires_auth
def create_actors():
    body = request.get_json()

    if not body:
        abort(400)

    new_name = body.get('name')
    new_age = body.get('age')
    new_gender = body.get('gender')

    if not new_name or not new_age or not new_gender:
        abort(400)

    try:

        new_actor = Actors(name=new_name, age=new_age, gender=new_gender)
        new_actor.insert()

        actors = Actors.query.order_by(Actors.id).all()
        current = [a.display() for a in actors]

        return jsonify({
            'title': 'Actors Page',
            'body': current,
            'success': True
        })
    except Exception as e:
        print(e)
        abort(422)


@actor.route('/actors/<int:actor_id>', methods=['DELETE', 'POST'])
#@requires_auth
def delete_actors(actor_id):
    actors = Actors.query.filter(Actors.id == actor_id).first()

    if not actors:
        abort(404)

    content_type = request.headers.get('Content-Type')

    try:
        actors.delete()

        if content_type == 'application/json':

            return jsonify({
                'title': 'Actors Page',
                'Deleted Actor': actor_id,
                'success': True
            })

        else:
            flash(f'Actor #{actor_id} was deleted successfully!', 'success')

    except Exception as e:
        print(e)

        if content_type == 'application/json':
            abort(422)

        else:
            flash(f'Cannot delete Actor #{actor_id} !', 'danger')

    return redirect(url_for('main.home'))


@actor.route('/actors/<int:actor_id>', methods=['PATCH'])
#@requires_auth
def update_actors(actor_id):
    actors = Actors.query.filter(Actors.id == actor_id).first()

    if not actors:
        abort(404)

    body = request.get_json()

    if not body:
        abort(400)

    updated_name = body.get('name')
    updated_age = body.get('age')
    updated_gender = body.get('gender')

    try:
        if updated_name:
            actors.name = updated_name
        if updated_age:
            actors.age = updated_age
        if updated_gender:
            actors.gender = updated_gender

        actors.update()

        actors = Actors.query.order_by(Actors.id).all()
        current = [a.display() for a in actors]

        return jsonify({
            'title': 'Actors Page',
            'body': current,
            'success': True
        })

    except Exception as e:
        print(e)
        abort(422)


# Forms/Templates type routes

@actor.route('/actors/create', methods=['GET'])
#@requires_auth
def create_actors_form():
    form = ActorsForm()
    return render_template('forms/new_actor.html', form=form, title='New Actor')


@actor.route('/actors/create', methods=['POST'])
#@requires_auth
def create_actors_submission():
    form = ActorsForm()
    if form.validate_on_submit():
        try:
            name = f'{request.form["first_name"]} {request.form["last_name"]}'
            a = Actors(
                name=name,
                age=request.form['age'],
                gender=request.form['gender']
            )

            a.insert()
            if request.form['gender'] == 'male':
                flash(f'Actor {name} has been listed successfully!', 'success')
            else:
                flash(f'Actress {name} has been listed successfully!', 'success')
            return redirect(url_for('main.home'))
        except Exception as e:
            print(e)
            flash('Cannot Create A New Actor!', 'danger')
    else:
        if 'age' in form.errors:
            error = 'Age must be an integer'
        else:
            error = 'Name must be a string'
        flash(f'Unable to create a new actor ({error}) !', 'warning')

    return render_template('forms/new_actor.html', title='New Actor', form=form)


@actor.route('/actors/<int:actor_id>/edit', methods=['GET'])
#@requires_auth
def update_actors_form(actor_id):
    form = ActorsForm()

    actor_ = Actors.query.filter(Actors.id == actor_id).first()
    if not actor_:
        abort(404)

    try:
        current = actor_.display()

        name = current['name']

        fullName = name.split()
        first_name = fullName[0]
        last_name = fullName[1]

        form.first_name.data = first_name
        form.last_name.data = last_name
        form.age.data = current['age']

        return render_template('forms/edit_actor.html', form=form, actor=current, title=f'Edit - {current["name"]}')

    except Exception as e:
        print(e)
        abort(422)


@actor.route('/actors/<int:actor_id>/edit', methods=['POST'])
#@requires_auth
def update_actors_submission(actor_id):
    form = ActorsForm()

    actor_ = Actors.query.filter(Actors.id == actor_id).first()
    if not actor_:
        abort(404)

    current = actor_.display()

    try:
        name = f'{request.form["first_name"]} {request.form["last_name"]}'
        if form.validate_on_submit():

            actor_.name = name
            actor_.age = request.form['age']
            actor_.gender = request.form['gender']

            actor_.update()
            if actor_.gender == 'male':
                flash(f'Actor {name} was successfully updated!', 'success')
            else:
                flash(f'Actress {name} was successfully updated!', 'success')
            return redirect(url_for('actors.get_actor', actor_id=actor_id))
        else:
            if request.form['gender'] == 'male':
                flash(f'An error occurred. Actor {current["name"]} could not be updated!', 'warning')
            else:
                flash(f'An error occurred. Actress {current["name"]} could not be updated!', 'warning')

        return render_template('forms/edit_actor.html', actor=current, form=form, title=f'Edit - {name}')
    except Exception as e:
        print(e)
        abort(422)

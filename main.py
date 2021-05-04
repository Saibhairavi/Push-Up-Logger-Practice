from . import db
from .models import User
from .models import Workout
from flask import Blueprint,render_template,url_for,request,redirect,flash
from flask_login import login_required,current_user

main=Blueprint('main',__name__)

@main.route('/')
def index():
    # return 'Hello World!'
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html',name=current_user.name)


#add new workout
@main.route('/new')
@login_required
def new_workout():
    return render_template('create_workout.html')

#ahandle post method of  new workout
@main.route('/new',methods=['POST'])
@login_required
def new_workout_post():

    #get the details from html page where user has entered details
    pushups=request.form.get('pushups')
    comment=request.form.get('comment')

    #add this in the database
    workout=Workout(pushups=pushups,comment=comment,author=current_user)
    db.session.add(workout)
    db.session.commit()
    flash('Your workout has been added')
    return redirect(url_for('main.user_workouts'))


@main.route('/all')
@login_required
def user_workouts():
    page=request.args.get('page',1,type=int)
    #url/?page=1 or /?page=4  like this

    user = User.query.filter_by(email=current_user.email).first_or_404()
    # workouts = user.workouts  
    # #to display all data in one page which is tedious to see

    # workouts_paginate=Workout.query.filter_by(author=user).order_by(Workout.date_posted.desc()).paginate(per_page=5)
    # #this is for pagination
    # print(dir(workouts_paginate))
    # print(workouts_paginate.items)
    # print(workouts_paginate.page)

    workouts=Workout.query.filter_by(author=user).paginate(page=page,per_page=3)
    return render_template('all_workouts.html', workouts=workouts, user=user)


#access each workout uniquely or a way  to have unique id for each workout
@main.route('/workout/<int:workout_id>/update',methods=['GET','POST'])
@login_required
def update_workout(workout_id):
    workout=Workout.query.get_or_404(workout_id)
    if request.method=='POST':
        workout.pushups=request.form['pushups']
        workout.comment=request.form['comment']
        db.session.commit()
        flash('Your workout has been updated!')
        return redirect(url_for('main.user_workouts'))
    return render_template('update_workout.html',workout=workout)

@main.route('/workout/<int:workout_id>/delete',methods=['GET','POST'])
@login_required
def delete_workout(workout_id):
    workout=Workout.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    flash('Your workout has been deleted!')
    return redirect(url_for('main.user_workouts'))



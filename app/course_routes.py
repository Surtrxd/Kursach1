from flask import Blueprint, request, redirect, url_for, render_template
from flask import flash, redirect, render_template, request, url_for
from .models import Course
from . import db

courses = Blueprint('courses', __name__)

@courses.route('/', methods=['GET'])
def get_courses():
    all_courses = Course.query.all()
    return render_template('courses.html', title="Курсы", courses=all_courses)

@courses.route('/add', methods=['GET'])
def add_course_page():
    return render_template('add_course.html', title="Добавить курс")

@courses.route('/add', methods=['POST'])
def add_course():
    title = request.form.get('title')
    description = request.form.get('description')
    new_course = Course(title=title, description=description)
    db.session.add(new_course)
    db.session.commit()
    return redirect(url_for('courses.get_courses'))

@courses.route('/delete/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for('courses.get_courses'))

@courses.route('/edit/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)  
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        if not title or not description:
            flash('Все поля должны быть заполнены!', 'error')
            return render_template('edit_course.html', course=course)
        course.title = title
        course.description = description
        db.session.commit()
        flash('Курс успешно обновлён!', 'success')
        return redirect(url_for('courses.get_courses'))
    return render_template('edit_course.html', course=course)


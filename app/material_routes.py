from flask import Blueprint, request, redirect, url_for, render_template
from .models import Material, Course
from . import db

materials = Blueprint('materials', __name__)

@materials.route('/materials/<int:course_id>', methods=['GET'])
def get_materials(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('materials.html', course=course, materials=course.materials)

@materials.route('/materials/add/<int:course_id>', methods=['GET'])
def add_material_page(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('add_material.html', course=course)

@materials.route('/materials/add/<int:course_id>', methods=['POST'])
def add_material(course_id):
    title = request.form.get('title')
    content = request.form.get('content')
    new_material = Material(title=title, content=content, course_id=course_id)
    db.session.add(new_material)
    db.session.commit()
    return redirect(url_for('materials.get_materials', course_id=course_id))

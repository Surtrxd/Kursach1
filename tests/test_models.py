import pytest
from app import create_app, db
from app.models import User, Course, Material, Test as TestModel
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    """Фикстура для создания Flask-приложения."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Используем in-memory SQLite для тестов
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Фикстура для предоставления тестового клиента."""
    return app.test_client()

def test_user_model(app):
    """Тест создания и проверки пользователя."""
    with app.app_context():
        user = User(
            username="testuser",
            email="testuser@example.com",
            password=generate_password_hash("password123")
        )
        db.session.add(user)
        db.session.commit()

        saved_user = User.query.filter_by(email="testuser@example.com").first()
        assert saved_user is not None
        assert saved_user.username == "testuser"
        assert saved_user.email == "testuser@example.com"

def test_course_model(app):
    """Тест создания и проверки курса."""
    with app.app_context():
        course = Course(
            title="Test Course",
            description="This is a test course description."
        )
        db.session.add(course)
        db.session.commit()

        saved_course = Course.query.filter_by(title="Test Course").first()
        assert saved_course is not None
        assert saved_course.description == "This is a test course description."

def test_material_model(app):
    """Тест создания и проверки учебного материала."""
    with app.app_context():
        course = Course(
            title="Test Course for Material",
            description="A course for material testing."
        )
        db.session.add(course)
        db.session.commit()

        material = Material(
            title="Test Material",
            content="This is test material content.",
            course_id=course.id
        )
        db.session.add(material)
        db.session.commit()

        saved_material = Material.query.filter_by(title="Test Material").first()
        assert saved_material is not None
        assert saved_material.content == "This is test material content."
        assert saved_material.course_id == course.id

def test_test_model(app):
    """Тест создания и проверки теста."""
    with app.app_context():
        test = TestModel(
            title="Test Title",
            questions="{'q1': 'What is Python?', 'q2': 'What is Flask?'}"
        )
        db.session.add(test)
        db.session.commit()

        saved_test = TestModel.query.filter_by(title="Test Title").first()
        assert saved_test is not None
        assert saved_test.questions == "{'q1': 'What is Python?', 'q2': 'What is Flask?'}"

def test_user_deletion(app):
    """Тест удаления пользователя."""
    with app.app_context():
        user = User(
            username="todelete",
            email="todelete@example.com",
            password=generate_password_hash("password123")
        )
        db.session.add(user)
        db.session.commit()

        db.session.delete(user)
        db.session.commit()

        deleted_user = User.query.filter_by(email="todelete@example.com").first()
        assert deleted_user is None

def test_course_update(app):
    """Тест обновления курса."""
    with app.app_context():
        course = Course(
            title="Original Title",
            description="Original Description"
        )
        db.session.add(course)
        db.session.commit()

        course.title = "Updated Title"
        course.description = "Updated Description"
        db.session.commit()

        updated_course = Course.query.filter_by(title="Updated Title").first()
        assert updated_course is not None
        assert updated_course.description == "Updated Description"

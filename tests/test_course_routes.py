import pytest
from app import create_app, db
from app.models import Course

@pytest.fixture
def app():
    """Создаёт тестовое приложение Flask."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Создаёт тестовый клиент Flask."""
    return app.test_client()

@pytest.fixture
def init_db(app):
    """Инициализирует базу данных с тестовыми данными."""
    with app.app_context():
        course1 = Course(title="Test Course 1", description="Test Description 1")
        course2 = Course(title="Test Course 2", description="Test Description 2")
        db.session.add_all([course1, course2])
        db.session.commit()
        yield db

def test_get_courses(client, init_db):
    response = client.get('/courses/')
    assert response.status_code == 200
    assert "Test Course 1" in response.data.decode("utf-8")
    assert "Test Course 2" in response.data.decode("utf-8")

def test_add_course(client, init_db):
    response = client.post('/courses/add', data={
        'title': 'New Course',
        'description': 'New Course Description'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "New Course" in response.data.decode("utf-8")


def test_edit_course(client, init_db):
    response = client.post('/courses/edit/1', data={
        'title': 'Updated Course Title',
        'description': 'Updated Course Description'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Updated Course Title" in response.data.decode("utf-8")
    assert "Updated Course Description" in response.data.decode("utf-8")

def test_edit_course_missing_fields(client, init_db):
    response = client.post('/courses/edit/1', data={
        'title': '',
        'description': ''
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Все поля должны быть заполнены!" in response.data.decode("utf-8")

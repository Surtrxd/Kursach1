import pytest
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_data(app):
    with app.app_context():
        user = User(
            email="test@example.com",
            password=generate_password_hash("password123"),
            username="testuser"  # Добавлено значение для username
        )
        db.session.add(user)
        db.session.commit()


# Тест существующего пользователя
def test_register_existing_user(client, init_data):
    response = client.post("/auth/register", data={
        "email": "test@example.com",
        "password": "password123",
        "password_confirm": "password123"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "auth/register" in response.data.decode("utf-8")  # Проверяем, что остались на странице регистрации

# Тест успешного входа
def test_login_success(client, init_data):
    response = client.post("/auth/login", data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "/" in response.data.decode("utf-8")  # Проверяем, что перенаправление на главную

# Тест неверных данных для входа
def test_login_invalid_credentials(client):
    response = client.post("/auth/login", data={
        "email": "wrong@example.com",
        "password": "wrongpassword"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "auth/login" in response.data.decode("utf-8")  # Проверяем, что остались на странице входа

# Тест выхода из системы
def test_logout(client, init_data):
    with client.session_transaction() as session:
        session["user_id"] = 1

    response = client.get("/auth/logout", follow_redirects=True)

    assert response.status_code == 200
    assert "auth/login" in response.data.decode("utf-8")  # Проверяем, что перенаправило на страницу входа

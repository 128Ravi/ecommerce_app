import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'testkey'
    
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['cart'] = {}
        yield client


# ---------------- ROUTE TESTS ---------------- #


def test_electronics_page(client):
    response = client.get('/')
    assert response.status_code == 200


def test_clothes_page(client):
    response = client.get('/clothes')
    assert response.status_code == 200
    assert b'Clothes' in response.data


def test_add_to_cart(client):
    response = client.get('/add_to_cart/1', follow_redirects=True)
    assert response.status_code == 200
    assert b'Laptop' in response.data


def test_cart_total_calculation(client):
    client.get('/add_to_cart/1')
    client.get('/add_to_cart/1')  # Add twice

    response = client.get('/cart')
    assert b'110000' in response.data  # 55000 x 2


def test_remove_from_cart(client):
    client.get('/add_to_cart/1', follow_redirects=True)
    client.get('/remove_from_cart/1', follow_redirects=True)

    response = client.get('/cart')

    # Cart should be empty (total = 0)
    assert b'Laptop' not in response.data



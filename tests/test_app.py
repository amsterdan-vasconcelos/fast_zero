from http import HTTPStatus


def test_root(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_user_created(client):
    response = client.post(
        '/users',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_user_find_all(client):
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'id': 1,
            }
        ]
    }


def test_user_update_username(client):
    """
    Atualiza o username do usuário.
    """
    response = client.patch('/users/1', json={'username': 'bruno'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bruno',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_user_delete(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.NO_CONTENT

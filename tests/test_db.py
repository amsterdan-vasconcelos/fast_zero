from dataclasses import asdict

from sqlalchemy import select

from fast_zero.user.models import User


def test_db_user_created(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='Ana', email='ana@email.com', password='secret'
        )
        session.add(new_user)
        session.commit()

        user = session.scalar(select(User).where(User.id == 1))

    assert asdict(user) == {
        'id': 1,
        'username': 'Ana',
        'email': 'ana@email.com',
        'password': 'secret',
        'created_at': time,
        'updated_at': time,
    }


def test_db_user_updated(session, mock_db_time):
    with mock_db_time(model=User) as time:
        create_user = User(
            username='Ana', email='ana@email.com', password='secret'
        )
        session.add(create_user)
        session.commit()

        created_user = session.scalar(select(User).where(User.id == 1))
        created_user.username = 'Amsterdan'
        session.commit()

        updated_user = session.scalar(select(User).where(User.id == 1))

    assert asdict(updated_user) == {
        'id': 1,
        'username': 'Amsterdan',
        'email': 'ana@email.com',
        'password': 'secret',
        'created_at': time,
        'updated_at': time,
    }

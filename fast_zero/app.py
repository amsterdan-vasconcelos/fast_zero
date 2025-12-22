from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.user import User, UserCreate, UserList, UserPublic, UserUpdate

app = FastAPI(title='Amsterdan Api')

database: list[User] = []


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserCreate):
    user_with_id = User(
        **user.model_dump(),
        id=len(database) + 1,
    )
    database.append(user_with_id)

    return user_with_id


@app.get('/users', status_code=HTTPStatus.OK, response_model=UserList)
def find_all_users():
    return {'users': database}


@app.patch('/users/{id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_users(id: int, user: UserUpdate):
    try:
        current_user = database[id - 1]
    except IndexError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    current_data = current_user.model_dump()
    update_data = user.model_dump(exclude_unset=True)
    merged_data = {**current_data, **update_data}
    updated_user = User.model_validate(merged_data)
    database[id - 1] = updated_user

    return updated_user


@app.delete('/users/{id}', status_code=HTTPStatus.NO_CONTENT)
def delete_users(id: int):
    try:
        database[id - 1]
    except IndexError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    del database[id - 1]

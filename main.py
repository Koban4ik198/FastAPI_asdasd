from fastapi import FastAPI, HTTPException
from config import db_settings
from models import User, Role
from response_models import UserCreate, UserRead
from sqlalchemy import select

app = FastAPI(
    title="FastAPI ORM Example",
    description="API для работы с пользователями и ролями",
    version="1.0.0",
    docs_url="/docs"
)

@app.get("/")
def read_root():
    return {"message": "FastAPI с SQLAlchemy работает!"}

@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int):
    with db_settings.get_session() as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

@app.post("/users/add", response_model=UserCreate)
def add_user(user_name: str, user_role: str):
    with db_settings.get_session() as session:
        # Ищем роль по имени
        role = session.execute(select(Role).where(Role.name == user_role)).scalar_one_or_none()
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        
        # Создаем пользователя
        new_user = User(name=user_name, role_id=role.id)
        session.add(new_user)
        session.commit()
        
        return UserCreate(name=user_name, role=user_role)
    
@app.put("/users/update/{user_id}")
def update_user(user_id: int, user_name: str, user_role: str):
    with db_settings.get_session() as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Ищем роль по имени
        role = session.execute(select(Role).where(Role.name == user_role)).scalar_one_or_none()
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        
        # Обновляем данные
        user.name = user_name
        user.role_id = role.id
        session.commit()
        
        return {"message": f"User {user_id} updated"}

@app.delete("/users/delete/{user_id}")
def delete_user(user_id: int):
    with db_settings.get_session() as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        session.delete(user)
        session.commit()
        
        return {"message": f"User {user_id} deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
from config import db_settings
from models import Role

# Добавляем роли в базу
with db_settings.get_session() as session:
    roles = ["user", "admin", "moderator"]
    for role_name in roles:
        role = Role(name=role_name)
        session.add(role)
    session.commit()
    print("✅ Тестовые роли добавлены!")
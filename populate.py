
from database.mongodb import user_collection
from controllers.user_controller import create_user


# user_collection().insert_one({
#         "username": "admin",
#         "role": "admin",
#         "email": "admin@example.com",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#     })

print(user_collection().find_one({"username": "admin"}))
print(create_user({
        "name": "UserName",
        "email": "user_email@test.com",
        "password": "1234",
        "role": "admin"
    }))
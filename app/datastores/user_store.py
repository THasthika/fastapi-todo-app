# import re
# import bcrypt
# from threading import Lock
# from uuid import uuid4, UUID
# from datetime import datetime
# from app.utils.meta import SingletonMeta
# from app.models.user import UserModel
# from app.schemas.user import UserCreate, UserUpdate

# ALLOWED_USERNAME_REGEX = r'^[a-zA-Z][a-zA-Z0-9\-]{3,}$'

# def _is_valid_username(username: str):
#     return re.match(ALLOWED_USERNAME_REGEX, username) is not None


# def _is_valid_password(password: str):
#     if len(str) < 8:
#         return False
#     return True


# def _hash_password(password: str):
#     return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


# def _check_password(check_password: str, password_hash: str):
#     return bcrypt.checkpw(check_password.encode(), password_hash)


# class UserStore(metaclass=SingletonMeta):

#     _users: list[UserModel]
#     _usernames: set[str]
#     _lock: Lock

#     def __init__(self) -> None:
#         self._users = []
#         self._usernames = set()
#         self._lock = Lock()

#     def create_user(self, user_create: UserCreate):

#         with self._lock:

#             # validate username
#             if not _is_valid_username(user_create.username):
#                 raise InvalidUsernameException()

#             # check if username is unique
#             if user_create.username in self._usernames:
#                 raise UsernameAlreadyExistsException()
            
#             # validate password
#             if not _is_valid_password(user_create.password):
#                 raise InvalidPasswordException()

#             # hash password
#             passowrd_hash = _hash_password(user_create.password)

#             user = UserModel(id=uuid4(),
#                              username=user_create.username,
#                              password=passowrd_hash,
#                              name=user_create.name,
#                              created_at=datetime.now(),
#                              updated_at=datetime.now())
            
#             self._users.append(user)
#             self._usernames.add(user_create.username)

#             return user
        
#     def get_user_by_username(self, username: str):

#         if username not in self._usernames:
#             raise UserNotFound()
        
#         for user in self._users:
#             if user.username == username:
#                 return user
    
#      def update_user(self, user_id: UUID, user_update: UserUpdate):

#         def _revert_changes_after_username_set():


#         with self._lock:
#             for user in self._users:
#                 if user.id == user_id:

#                     # handle username check
#                     if user_update.username is not None:
#                         self._usernames.remove(user.username)
#                         if user_update.username in self._usernames:
#                             self._usernames.add(user.username)
#                             raise UsernameAlreadyExistsException()      
#                         user.username = user_update.username

#                     # handle password update
#                     if user_update.password is not None:


#                     user.name = user_update.name
#                     user.updated_at = datetime.now()
#                     return user
#             raise UserNotFound()

#     def delete_user(self, user_id: UUID):
#         with self._lock:
#             for user in self._users:
#                 if user.id == user_id:
#                     self._users.remove(user)
#                     self._usernames.remove(user.username)
#                     return
#             raise UserNotFound()
        
    

# class UsernameAlreadyExistsException(Exception):
#     pass


# class InvalidUsernameException(Exception):
#     pass


# class InvalidPasswordException(Exception):
#     pass


# class UserNotFound(Exception):
#     pass
from models.user import User


class Users_container:
    def __init__(self):
        self.users = list()

    def users_amount(self):
        return len(self.users)

    def add_user(self, user: User):
        self.users.append(user)

    def get_user(self, id) -> User:
        return self.users[id]

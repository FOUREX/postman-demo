users = {}


class Context:
    @staticmethod
    def get_users() -> list:
        return list(users.keys())

    @staticmethod
    def get_user(name: str) -> dict | None:
        return users.get(name.lower())

    @staticmethod
    def add_user(name: str, password: str) -> bool:
        if name.lower() in users:
            return False

        users[name.lower()] = {
            "display_name": name,
            "password": password
        }

        return True

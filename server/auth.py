USERS = {
    "Condurache": "Gabriel",
    "Bandur": "Mihai",
    "Bejenariu": "Codrin"
} # 3 conturi de autentificare unice tip lider

def check_login(username:str, password:str) -> bool:
    return USERS.get(username) == password

def create_user(username: str, password: str) -> bool:
    if username in USERS:
        return False
    USERS[username] = password
    return True
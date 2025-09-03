USERS = {
    "Condurache": "Gabriel",
    "Bandur": "Mihai",
    "Bejenariu": "Codrin"
}

def check_login(username:str, password:str) -> bool:
    return USERS.get(username) == password
from dataclasses import dataclass


@dataclass
class UserLogin:
    login: str
    password: str

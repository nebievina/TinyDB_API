
import re
import string
from tinydb import TinyDB, where
from pathlib import Path
from typing import List


class User:

    DB = TinyDB(Path(__file__).resolve().parent / "db.json", indent=4)

    def __init__(self, first_name: str, last_name: str, phone_number: str="", address: str=""):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address

    def __str__(self):
        return f"{self.full_name}\n{self.phone_number}\n{self.address}"

    def __repr__(self):
        return f"{User(self.first_name, self.last_name)}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def db_instance(self):
        return User.DB.get((where("first_name") == self.first_name) & (where("last_name") == self.last_name))

    def _check(self):
        self._check_names()
        self._check_phone_number()

    def _check_phone_number(self):
        phone_digits = re.sub(r"[+()\s]", "", self.phone_number)
        if len(phone_digits) < 10 or not phone_digits.isdigit():
            raise ValueError (f"Numero de telephone {self.phone_number} invalide.")
        print(phone_digits)

    def _check_names(self):
        if not (self.first_name and self.last_name):
            raise ValueError ("Le prenom et le nom de famille doivent est valide")
        special_character = string.punctuation + string.digits
        full_name = self.first_name + self.last_name

        if set(full_name)&set(special_character):
            raise ValueError ("Le nom et le prenom ne doivent etre fait que de lettres")

    def save(self, validate_data: bool=False) -> int:
        if validate_data:
            self._check()
        
        if self.exists():
            return -1
        else:
            return(User.DB.insert(self.__dict__))

    def exists(self):
        return bool(self.db_instance)

    def delete(self) -> List[int]:
        if self.exists() :
            return User.DB.remove(doc_ids=[self.db_instance.doc_id])
        return []

def get_all_users():
    return [User(**user) for user in User.DB.all()]


if __name__ == "__main__":
    # from faker import Faker
    # fake = Faker(locale="de_DE")

    # for _ in range(10):
    #     user = User(
    #         first_name = fake.first_name(), 
    #         last_name = fake.last_name(), 
    #         phone_number = fake.phone_number(), 
    #         address = fake.address()
    #         )
    ivonne = User("Ivonne", "Ehlert")
    #   "first_name": "Ivonne",
    #         "last_name": "Ehlert",
    print(print(ivonne.delete()))
        # print("-"*10)
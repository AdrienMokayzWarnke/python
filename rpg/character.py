import json
from typing import List

class Classe:
    def __init__(self, name, hp, mana, rage, sorts, description):
        self.name = name
        self.hp = hp
        self.mana = mana
        self.rage = rage
        self.sorts = sorts
        self.description = description

    def __repr__(self):
        return f"Classe(name={self.name}, hp={self.hp}, mana={self.mana}, rage={self.rage}, sorts={self.sorts}, description={self.description})"

class Sort:
    def __init__(self, id, name, cout_mana, cout_rage, degat, soin, cible):
        self.id = id
        self.name = name
        self.cout_mana = cout_mana
        self.cout_rage = cout_rage
        self.degat = degat
        self.soin = soin
        self.cible = cible

    def __repr__(self):
        return f"Sort(id={self.id}, name={self.name}, cout_mana={self.cout_mana}, cout_rage={self.cout_rage}, degat={self.degat}, soin={self.soin}, cible={self.cible})"

class Character:
    def __init__(self, name: str, char_class: Classe):
        self.name = name
        self.char_class = char_class.name
        self.hp = char_class.hp
        self.mana = char_class.mana
        self.rage = char_class.rage
        self.sorts = [SORTS[id-1] for id in char_class.sorts]

    def __repr__(self):
        return f"Character(name={self.name}, classe={self.char_class}, hp={self.hp}, mana={self.mana}, rage={self.rage}, sorts={self.sorts})"

def load_classes(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        classes_data = json.load(file)
        classes = [Classe(**data) for data in classes_data["classes"]]
        return classes

def load_sorts(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        sorts_data = json.load(file)
        sorts = [Sort(**data) for data in sorts_data["sorts"]]
        return sorts

def get_class_by_name(class_name):
    return next((classe for classe in CLASSES if classe.name == class_name), None)

def create_character(name, class_name):
    char_class = get_class_by_name(class_name)
    if char_class:
        return Character(name, char_class)
    
# Load classes and sorts from JSON files
CLASSES: List[Classe] = load_classes('data/classe.json')
SORTS: List[Sort] = load_sorts('data/sorts.json')


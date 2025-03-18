import json

class Enemy:
    def __init__(self, id, name, hp, mana, rage, sorts, description):
        self.id = id
        self.name = name
        self.hp = hp
        self.mana = mana
        self.rage = rage
        self.sorts = sorts
        self.description = description

    def __repr__(self):
        return (f"Enemy(id={self.id}, name={self.name}, hp={self.hp}, mana={self.mana}, "
                f"rage={self.rage}, sorts={self.sorts}, description={self.description})")

    def take_damage(self, damage):
        self.hp -= max(0, damage - self.defense)
        if self.hp < 0:
            self.hp = 0

    def is_alive(self):
        return self.hp > 0

def load_enemies_from_json(file_path):
    with open(file_path, 'r') as file:
        enemies_data = json.load(file)
        enemies = [Enemy(**data) for data in enemies_data]
    return enemies

# Example usage:
# enemies = load_enemies_from_json('enemies.json')
# for enemy in enemies:
#     print(enemy)
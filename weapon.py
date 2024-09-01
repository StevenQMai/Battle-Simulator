class Weapon:
    def __init__(self, 
                name: str, 
                weapon_type: str, 
                damage: int, 
                value: int):
        self.name = name
        self.weapon_type = weapon_type
        self.damage = damage
        self.value = value

iron_sword = Weapon(name="Iron Sword", 
                    weapon_type="Sharp", 
                    damage=5, 
                    value=10)

short_bow = Weapon(name="Short Bow", 
                    weapon_type="Ranged", 
                    damage=3, 
                    value=5)

fists = Weapon(name="Fists", 
                    weapon_type="Blunt", 
                    damage=1, 
                    value=0)


available_weapons = [iron_sword, short_bow, fists]
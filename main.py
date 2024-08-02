import os
from character import Hero, Enemy
from weapon import *
import random

hero = Hero(name="Hero",  health=100)
enemy = Enemy(name="Enemy",  health=50, weapon=None)

print("Choose a weapon for the hero!\n")
for index, weapon in enumerate(available_weapons):
    print(f"{index + 1}: {weapon.name} (Type: {weapon.weapon_type}, Damage: {weapon.damage})")

choice = int(input("\nEnter your weapon ID: ")) - 1
chosen_weapon = available_weapons[choice]
hero = Hero(name="Hero", health=100)
hero.equip(available_weapons[choice])

enemy_weapon = random.choice(available_weapons)
enemy = Enemy(name="Enemy", health=50, weapon=enemy_weapon)


while True:
    os.system("clear")

    print(f"\nThe hero has chosen [{chosen_weapon.name}]!") #chosen_weapon contains attributes related to a weapon (name, type, damage, value)
                                                            #chosen_weapon.name accesses the 'name' attribute of the 'chosen_weapon' object
    print(f"The enemy has [{enemy_weapon.name}]!\n")

    hero.attack(enemy)
    enemy.attack(hero)

    hero.health_bar.update()
    enemy.health_bar.update()
    hero.health_bar.draw()
    enemy.health_bar.draw()


    user_input = input("Press 'g' to drop your weapon \nPress [ENTER] to Continue The Battle...\n")
    if user_input == "g":
        hero.drop()
        print("The hero has dropped their weapon!")


    if hero.health <= 0 or enemy.health <= 0:
        if hero.health > 0:
            victor = hero.name
        elif enemy.health > 0:
            victor = enemy.name
        else:
            victor = "IT'S A DRAW!"
        print("GAME OVER!")
        print(f"The winner is the {victor}!")
        break

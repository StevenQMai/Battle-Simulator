import os
from character import Hero, Enemy
from weapon import *
import random
import time

class Game:
    def __init__(self):
        self.hero = Hero(name="Hero", health=100)
        self.enemy = Enemy(name="Enemy", health=50, weapon=None)
        self.hero_weapon = None
        self.enemy_weapon = None

    def display_weapons(self):
        print("Choose a weapon for the hero!\n")
        for index, weapon in enumerate(available_weapons):
            print(f"{index + 1}. {weapon.name}\n Type: {weapon.weapon_type}, Damage: {weapon.damage}")

    def choose_weapon(self):
        choice = int(input("\nEnter your weapon ID: \n")) - 1
        chosen_weapon = available_weapons[choice]
        self.hero.equip(chosen_weapon)

    def enemy_weapon_choice(self):
        enemy_weapon = random.choice(available_weapons)
        self.enemy.weapon = enemy_weapon
        print(f"The enemy has chosen a(n) {enemy_weapon.name}!\n")

    def startBattle(self):
        self.enemy_weapon_choice()
        while True:
            os.system("clear")

            self.hero.attack(self.enemy)
            self.enemy.attack(self.hero)

            self.hero.health_bar.update()
            self.enemy.health_bar.update()
            self.hero.health_bar.draw()
            self.enemy.health_bar.draw()

            user_input = input("Press 'g' to drop your weapon \nPress [ENTER] to Continue The Battle...\n")
            if user_input == "g":
                self.hero.drop()
                print("The hero has dropped their weapon!")
                time.sleep(3)

            if self.hero.health <= 0 or self.enemy.health <= 0:
                if self.hero.health > 0:
                    victor = self.hero.name
                elif self.enemy.health > 0:
                    victor = self.enemy.name
                else:
                    victor = "IT'S A DRAW!"
                print("GAME OVER!")
                print(f"The winner is the {victor}!")
                break





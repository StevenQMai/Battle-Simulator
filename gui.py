import pygame as pg
from game_logic import Game
from character import Hero, Enemy
from health_bar import *
from weapon import *
import random
import sys
import os

class Button:
    def __init__(
        self, 
        screen, 
        x, 
        y, 
        width, 
        height, 
        text, 
        font, 
        button_shade_light, 
        button_shade_dark):
        self.screen = screen
        self.rect = pg.Rect(x,y,width,height)
        self.text = text
        self.font = font
        self.button_shade_light = button_shade_light
        self.button_shade_dark = button_shade_dark
        self.text_render = self.font.render(self.text, True, pg.Color("White"))

    def draw(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            pg.draw.rect(surface=self.screen, color=self.button_shade_light, rect=self.rect)
        else:
            pg.draw.rect(surface=self.screen, color=self.button_shade_dark, rect=self.rect)

            text_rect = self.text_render.get_rect(center=self.rect.center)
            self.screen.blit(self.text_render, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class TextBox:
    def __init__(self, screen, x, y, width, height, text, font, bg_color, text_color):
        self.screen = screen
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color

    def draw(self):
        # Draw the background rectangle
        pg.draw.rect(self.screen, self.bg_color, self.rect)
        # Render the text
        self.render_text()

    def render_text(self):
        # Split text into multiple lines if necessary
        lines = self.wrap_text(self.text, self.rect.width - 20)  # 20 pixels padding
        y_offset = self.rect.top + 10  # 10 pixels padding from top

        for line in lines:
            text_surf = self.font.render(line, True, self.text_color)
            self.screen.blit(text_surf, (self.rect.left + 10, y_offset))  # 10 pixels padding from left
            y_offset += text_surf.get_height()  # Move down for the next line

    def wrap_text(self, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            test_surface = self.font.render(test_line, True, pg.Color("White"))

            if test_surface.get_width() <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines



class GUI:
    def __init__(self):
        pg.init()
        self.width = 800
        self.height = 500
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Battle Simulator!")

        #self.background_color = pg.Color("white")
        self.background_images = {
            "weapon_selection": pg.image.load(os.path.join("weapon_selection.png")).convert_alpha(),
            "battle": pg.image.load(os.path.join("battle_background.png")).convert_alpha()
            }
        self.current_background = self.background_images["weapon_selection"]
    
        self.small_font = pg.font.SysFont("Corbel", 50)

        self.title_box = TextBox(
            screen=self.screen,
            x=50,
            y=self.height//2 - 50,
            width=self.width//2,
            height=60,
            text="Select your weapon!",
            font=self.small_font,
            bg_color=(135, 206, 235),  # Sky blue background
            text_color=(255, 255, 255)  # White text
        )

        self.message_box_height = 150
        self.message_box = pg.Surface((self.width, self.message_box_height))
        self.message_box.fill(pg.Color("black"))

        self.messages = []
        self.message_display_duration = 2000

        self.fight_button = Button(self.screen, self.width//1.4, self.height//1.7, 200, 100, "Fight", self.small_font, (170, 170, 170), (100,100,100))
        self.drop_button = Button(self.screen, self.width//1.4, self.height//1.3, 200, 100, "Drop", self.small_font, (170, 170, 170), (100,100,100))

        self.weapons_button = []
        self.create_weapon_buttons()

        self.running = True
        self.state = "weapon_selection"

        self.game = Game()

        self.hero_health_bar = HealthBar(self.game.hero, 50, 15, 200, 30, self.game.hero.health_max, (0, 255, 0))
        self.enemy_health_bar = HealthBar(self.game.enemy, 50, 50, 200, 30, self.game.enemy.health_max, (255, 0, 0))

        self.run_game() 

    def update_background(self):
        # Scale the background image to fit the current window size
        self.background = pg.transform.scale(self.current_background, (self.width, self.height))
        

    def run_game(self):
        while self.running:
            self.check_events()
            self.update_background()
            self.update_screen()


    def create_weapon_buttons(self):
        for index, weapon in enumerate(available_weapons):
            button = Button(
                screen=self.screen,
                x=550,
                y=200 + index * 60,
                width=200,
                height=50,
                text=weapon.name,
                font=self.small_font,
                button_shade_light=(170,170,170),
                button_shade_dark=(100,100,100)
            )
            self.weapons_button.append((button,weapon))


    def check_events(self):
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                self.quit_game()

            if event.type == pg.MOUSEBUTTONDOWN:
                if self.state == "weapon_selection":
                    self.check_weapon_selection(mouse_pos)
                elif self.state == "battle":
                    self.check_battle_events(mouse_pos)



    def check_weapon_selection(self, mouse_pos):
        for button, weapon in self.weapons_button:
            if button.is_clicked(mouse_pos):
                self.game.hero.equip(weapon)
                self.show_message(f"{weapon.name} equipped!", 2000)
                self.state = "battle"
                self.current_background = self.background_images["battle"]
                self.game.enemy_weapon_choice()



    def check_battle_events(self, mouse_pos):
        if self.fight_button.is_clicked(mouse_pos):
            self.messages.clear()

            self.game.hero.attack(self.game.enemy)
            self.show_message(f"{self.game.hero.name} dealt {self.game.enemy.last_damage} damage to {self.game.enemy.name}!", 500)

            self.game.enemy.attack(self.game.hero)
            self.show_message(f"{self.game.enemy.name} dealt {self.game.hero.last_damage} damage to {self.game.hero.name}!", 500)

            if self.game.hero.health <= 0 or self.game.enemy.health <= 0:
                self.running = False
                self.show_game_over()
        elif self.drop_button.is_clicked(mouse_pos):
            self.game.hero.drop()
            print("The hero has dropped their weapon!")



    def update_screen(self):
        self.screen.blit(self.background, (0,0))
        mouse_pos = pg.mouse.get_pos()

        if self.state == "weapon_selection":
            self.title_box.draw()
            self.update_weapon_selection_screen(mouse_pos)


        elif self.state == "battle":
            self.screen.blit(self.background_images["battle"], (0, 0))
            self.update_battle_screen(mouse_pos)

            message_box_x = 0
            message_box_width = self.width - (self.width // 3) + 10   # Keep space for action buttons

            # Update the message box dimensions and position
            self.message_box = pg.Surface((message_box_width, self.message_box_height))
            self.message_box.fill(pg.Color("black"))

            #draws a message box that spawns when the battle state starts
            self.screen.blit(self.message_box, (0, self.height - self.message_box_height))

            current_time = pg.time.get_ticks()
            self.messages = [msg for msg in self.messages if msg[1] > current_time]  # Remove expired messages
            #Filters out messages that have expired (i.e., their display duration has passed). 
            #Only messages with a timestamp greater than the current time are kept in the self.messages list.


            y_offset = self.height - self.message_box_height + 10  # Starting y position for messages
            for message, _ in self.messages:
                text_surf = self.small_font.render(message, True, pg.Color("white"))
                self.screen.blit(text_surf, (message_box_x, y_offset))
                y_offset += text_surf.get_height() + 8  # Adjust y position for next message

        pg.display.update()


    def update_weapon_selection_screen(self, mouse_pos):
        for button, _ in self.weapons_button:
            button.draw(mouse_pos)

    def update_battle_screen(self, mouse_pos):

        self.fight_button.draw(mouse_pos)
        self.drop_button.draw(mouse_pos)

        self.hero_health_bar.update()
        self.enemy_health_bar.update()
        self.hero_health_bar.draw(self.screen)
        self.enemy_health_bar.draw(self.screen)


    def show_message(self, message, duration):
        self.messages.append((message, pg.time.get_ticks() + duration))



    def show_game_over(self):
        if self.game.hero.health > 0:
            victor = self.game.hero.name
        elif self.enemy.health > 0:
            victor = self.game.enemy.name
        else:
            victor = "IT'S A DRAW!"
        
        game_over_text = self.small_font.render(f"GAME OVER! The {victor} wins!", True, pg.Color("white"))
        self.screen.fill(pg.Color("black"))
        self.screen.blit(game_over_text, (self.width // 2 - game_over_text.get_width() // 2, self.height // 2))

        pg.display.update()
        pg.time.wait(3000)
        self.quit_game()


    def quit_game(self):
        pg.quit()
        sys.exit()



if __name__ == "__main__":
    GUI()
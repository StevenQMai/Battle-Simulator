import os
import pygame as pg

os.system("")    

class HealthBar:
    symbol_remaining: str = "█"
    symbol_lost: str = "_"
    barrier: str = "|"
    colors: dict = {"red" : "\033[91m",
                    "purple" : "\33[95m",
                    "blue" : "\33[34m",
                    "blue2" : "\33[36m",
                    "blue3" : "\33[96m",
                    "green" : "\033[92m",
                    "green2" : "\033[32m",
                    "brown" : "\33[33m",
                    "yellow" : "\33[93m",
                    "grey" : "\33[37m",
                    "default" : "\033[0m",
                    }

    def __init__(self,
                entity,
                x, 
                y,
                width,
                height,
                max_health,
                color):
        self.entity = entity
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.color = color
        self.background_color = (0,0,0)   

    def update(self):
        pass


    def draw(self, screen):

        health_percentage = self.entity.health / self.max_health
        bar_width = int(self.width * health_percentage)

        pg.draw.rect(screen, self.background_color, (self.x, self.y, self.width, self.height))
        pg.draw.rect(screen, self.color, (self.x, self.y, bar_width, self.height))

        """
        remaining_bars = round(self.current_value / self.max_value * self.length)
        lost_bars = self.length - remaining_bars
        print(f"\n{self.entity.name}'s HEALTH: {self.entity.health}/{self.entity.health_max}")
        print(f"{self.barrier}" 
              f"{self.color if self.is_colored else ''}"
              f"{remaining_bars * self.symbol_remaining}"
              f"{lost_bars * self.symbol_lost}"
              f"{self.colors['default'] if self.is_colored else ''}"
              f"{self.barrier}\n")
        """
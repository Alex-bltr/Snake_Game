import time
import pygame
import random
import tkinter as tk
from tkinter import *
import math
import sys


WINDOW_SIZE = 600
GRID_SIZE = 20
RECT_SIZE = 30
STEP_SIZE = 3
FPS = 60

class Menu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("400x400")
        self.root.title("Menu")

    def options(self):
        self.root.mainloop()

class Ground:
    def __init__(self):
        pygame.init()
        self.ground = pygame.display.set_mode((660,740))
        self.Background = pygame.Rect(0, 80, 660, 660)
        pygame.display.set_caption("SNAKE!")
        self.clock = pygame.time.Clock()
        self.running = True
        self.row_num = GRID_SIZE
        self.col_num = GRID_SIZE
        self.rectv = RECT_SIZE
        self.step = STEP_SIZE
        self.snake = [pygame.Rect(5 * self.rectv+30, 10 * self.rectv+110, self.rectv, self.rectv)]
        self.Direction = "RIGHT"
        self.opposite_dir = {"LEFT": "RIGHT", "RIGHT": "LEFT", "UP": "DOWN", "DOWN": "UP"}
        self.fruit_counter = 0
        self.fruit_rect = None
        self.pending_direction = None
        self.big_fruit_img = pygame.image.load("C:\\Users\\alexg\\Downloads\\apple.png").convert_alpha()
        self.big_fruit = pygame.transform.scale(self.big_fruit_img, (55, 55))
        self.big_apple_rect= self.big_fruit.get_rect(center=(60, 40))
        self.crunch_sound = pygame.mixer.Sound("C:\\Users\\alexg\\Downloads\\crunch.wav")
        self.sound = True
        self.sound_img = pygame.image.load("C:\\Users\\alexg\\Downloads\\sound_on-removebg-preview.png").convert_alpha()
        self.sound_img = pygame.transform.scale(self.sound_img, (40, 40))
        self.sound_off_img = pygame.image.load("C:\\Users\\alexg\\Downloads\\sound_off-removebg-preview.png").convert_alpha()
        self.sound_off_img = pygame.transform.scale(self.sound_off_img, (44,44))
        self.button_on_rect = self.sound_img.get_rect(center=(580, 40))
        self.button_off_rect = self.sound_off_img.get_rect(center=(580, 40))
        self.font = pygame.font.SysFont(None, 45)
        self.score = 0
        self.fruit_image = pygame.image.load("C:\\Users\\alexg\\Pictures\\apfelspiel.png").convert_alpha()
        self.final_fruit = pygame.transform.scale(self.fruit_image, (30, 30))

        self.trophy_img = pygame.image.load("C:\\Users\\alexg\\Pictures\\2317448.png").convert_alpha()
        self.trophy = pygame.transform.scale(self.trophy_img, (45, 45))
        self.trophy_rect = self.trophy.get_rect(center=(160, 40))

        

    def make_ground(self):
        for row in range(self.row_num):
            for col in range(self.col_num):
                color = "#AAD751" if (col + row) % 2 == 0 else "#A2D149"
                pygame.draw.rect(self.ground, color, pygame.Rect(col * self.rectv+30, row * self.rectv+110, self.rectv, self.rectv))

    def play_crunch_sound(self):
        self.crunch_sound.play()
    
    def sound_button_update(self):
        if self.sound == True:
            self.ground.blit(self.sound_img, self.button_on_rect)
            print("Sound an")
        else:
            self.ground.blit(self.sound_off_img, self.button_off_rect)
            print("Sound aus")

    def spawn_fruit(self):
        if self.fruit_counter == 0:
            self.fruit_counter += 1
            while True:
                centerx = random.randint(1, 19) * self.rectv + 15+30
                centery = random.randint(1, 19) * self.rectv + 15+110
                if not any(cube.collidepoint(centerx, centery) for cube in self.snake):
                    break
            self.fruit_rect = self.final_fruit.get_rect(center=(centerx, centery))
        if self.fruit_rect:
            self.ground.blit(self.final_fruit, self.fruit_rect)
    
    def snake_spawn(self, angle):
        head_rect = self.snake[0]

        for i, segment in enumerate(self.snake):
            if i == 0:
                # Head with eyes and nose
                pygame.draw.rect(self.ground, "#5870db", segment, border_radius=9)
            else:
                tl_r, tr_r, bl_r, br_r = 9, 9, 9, 9  # Standard corners
                pygame.draw.rect(self.ground, "#5870db", segment,
                                border_top_left_radius=tl_r,
                                border_top_right_radius=tr_r,
                                border_bottom_left_radius=bl_r,
                                border_bottom_right_radius=br_r)

    def move(self):
        if not hasattr(self, "positions"):
            self.positions = []

        self.positions.append((self.snake[0].x, self.snake[0].y))

        max_positions = len(self.snake) * self.rectv // self.step
        if len(self.positions) > max_positions:
            self.positions.pop(0)

        if self.pending_direction and (self.snake[0].x-30) % self.rectv == 0 and (self.snake[0].y-110) % self.rectv == 0:
            self.Direction = self.pending_direction
            self.pending_direction = None

        step = self.step
        if self.Direction == "RIGHT":
            self.snake[0].x += step
        elif self.Direction == "LEFT":
            self.snake[0].x -= step
        elif self.Direction == "UP":
            self.snake[0].y -= step
        elif self.Direction == "DOWN":
            self.snake[0].y += step

        for i in range(1, len(self.snake)):
            target_index = ((i * self.rectv) // self.step)
            segment_target = self.positions[target_index]

            follower = self.snake[i]
            diff_x = segment_target[0] - follower.x
            diff_y = segment_target[1] - follower.y

            follower.x += diff_x
            follower.y += diff_y

    def borderpatrol(self):
        if (self.snake[0].x < 30 or self.snake[0].x > self.col_num * self.rectv or
                self.snake[0].y < 110 or self.snake[0].y > self.row_num * self.rectv+80):
            self.running = False

    def direction_angle(self, dir):
        return {"LEFT": 270, "RIGHT": 90, "UP": 180, "DOWN": 0}[dir]

    def gaming(self):
        self.make_ground()
        self.move()
        self.snake_spawn(self.direction_angle(self.Direction))
        self.spawn_fruit()

        if self.snake[0].colliderect(self.fruit_rect):
            self.fruit_rect = None
            self.snake.append(self.snake[-1].copy())
            if self.sound == True:
                self.play_crunch_sound()
            self.fruit_counter = 0
            self.score += 1
        elif self.snake[0] in self.snake[1:]:
            #mit pygame kann man das so direkt prüfen 
            self.running = False

        pygame.display.flip()
        self.clock.tick(FPS)
        self.borderpatrol()

    def spawn(self):
        while self.running:
            self.ground.fill("#4a752c")
            pygame.draw.rect(self.ground, "#578a34", self.Background)
            self.ground.blit(self.big_fruit, self.big_apple_rect)
            self.score_text = self.font.render(f"{self.score}", True, "white")
            self.score_text_rect = self.score_text.get_rect(center=(105, 50))
            self.record_text = self.font.render(f"{self.score}", True, "white")
            self.record_text_rect = self.record_text.get_rect(center=(200,50))
            self.ground.blit(self.record_text, self.record_text_rect)
            self.ground.blit(self.score_text, self.score_text_rect)
            self.ground.blit(self.trophy, self.trophy_rect)
            self.sound_button_update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sound and self.button_on_rect.collidepoint(event.pos):
                        self.sound = False
                    elif not self.sound and self.button_off_rect.collidepoint(event.pos):
                        self.sound = True
                elif event.type == pygame.KEYDOWN:
                    new_direction = None
                    if event.key == pygame.K_RIGHT:
                        new_direction = "RIGHT"
                    elif event.key == pygame.K_LEFT:
                        new_direction = "LEFT"
                    elif event.key == pygame.K_DOWN:
                        new_direction = "DOWN"
                    elif event.key == pygame.K_UP:
                        new_direction = "UP"
                    if new_direction and new_direction != self.opposite_dir[self.Direction]:
                        self.pending_direction = new_direction

            self.gaming()
if __name__ == "__main__":
    print("Starte Spiel")
    try:
        menu = Menu()
        menu.options()
        game = Ground()
        game.spawn()
    except Exception as e:
        print(f"Fehler: {e}")
    print("Spiel beendet")

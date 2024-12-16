import time
import pygame  
import random
import tkinter as tk
from tkinter import *

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
        self.ground = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("SNAKE!")
        self.clock = pygame.time.Clock()
        self.running = True
        self.color = ""
        self.row_num = 20
        self.col_num = 20
        self.snake_start_x = 5
        self.snake_start_y = 10
        self.rectv = 30
        self.snake = [pygame.Rect(self.snake_start_x * self.rectv, self.snake_start_y * self.rectv, self.rectv-3, self.rectv-3)]
        self.Direction = "RIGHT"
        self.opossite_dir = {
            "LEFT": "RIGHT",
            "RIGHT": "LEFT",
            "UP": "DOWN",
            "DOWN": "UP"
        }
        
       
        self.eyes_image = pygame.image.load("C:\\Users\\alexg\\Pictures\\snake_eyes0.webp").convert_alpha()
        self.eyes_final = pygame.transform.scale(self.eyes_image, (30, 30))
        self.Nase_image = pygame.image.load("C:\\Users\\alexg\\Pictures\\Snake_nasepng.png").convert_alpha()
        self.final_nose = pygame.transform.scale(self.Nase_image, (10, 10))

        self.fruit = pygame.image.load("C:\\Users\\alexg\\Pictures\\cherry-pixel-art-png.webp").convert_alpha()
        self.final_fruit = pygame.transform.scale(self.fruit, (30, 30))
        self.fruit_rect = None  
        self.fruit_counter = 0



    def spawn_fruit(self):
        if self.fruit_counter == 0:
            self.fruit_counter += 1
            self.spawnclearing = True  

            while self.spawnclearing:
                centerx = random.randint(1, 19) * 30 + 15
                centery = random.randint(1, 19) * 30 + 15
                self.spawnclearing = True

                
                for cube in self.snake:
                    if cube.centerx != centerx and cube.centery != centery:
                        self.spawnclearing = False

            self.fruit_rect = self.final_fruit.get_rect(center=(centerx, centery))
            centerx = NONE
            centery = NONE

        if self.fruit_rect:
            self.fruit_c = self.ground.blit(self.final_fruit, self.fruit_rect)
    
    

    def snake_spawn(self, winkel):
        
        head_rect = self.snake[0]
        self.rotated_eyes = pygame.transform.rotate(self.eyes_final, winkel)
        self.rotated_augen_f = self.rotated_eyes.get_rect(center=(head_rect.centerx, head_rect.centery - 15))
        
        self.rotated_nose = pygame.transform.rotate(self.final_nose, winkel)
        self.rotated_Nase_f = self.rotated_nose.get_rect(center=(head_rect.centerx, head_rect.centery + 15))
        if winkel == 90:
            for i, segment in enumerate(self.snake):
                if i == 0:  # Kopf
                    pygame.draw.rect(self.ground, "#5870db", segment, border_top_right_radius=self.rectv, border_bottom_right_radius=self.rectv)
                    self.ground.blit(self.rotated_eyes, self.rotated_augen_f)
                    self.ground.blit(self.rotated_nose, self.rotated_Nase_f)
                else: 
                    pygame.draw.rect(self.ground, "#5870db", segment )
                
        elif winkel == 0:
            for i, segment in enumerate(self.snake):
                if i == 0:  # Kopf
                        pygame.draw.rect(self.ground, "#5870db", segment, border_bottom_left_radius=self.rectv, border_bottom_right_radius=self.rectv)
                        self.ground.blit(self.rotated_eyes, self.rotated_augen_f)
                        self.ground.blit(self.rotated_nose, self.rotated_Nase_f)
                else: 
                    pygame.draw.rect(self.ground, "#5870db", segment )
        elif winkel == 180:
            for i, segment in enumerate(self.snake):
                if i == 0:  # Kopf
                        pygame.draw.rect(self.ground, "#5870db", segment, border_top_right_radius=self.rectv, border_top_left_radius=self.rectv)
                        self.ground.blit(self.rotated_eyes, self.rotated_augen_f)
                        self.ground.blit(self.rotated_nose, self.rotated_Nase_f)
                else: 
                    pygame.draw.rect(self.ground, "#5870db", segment )
        elif winkel == 270:
            for i, segment in enumerate(self.snake):
                if i == 0:  # Kopf
                        pygame.draw.rect(self.ground, "#5870db", segment, border_top_left_radius=self.rectv, border_bottom_left_radius=self.rectv)
                        self.ground.blit(self.rotated_eyes, self.rotated_augen_f)
                        self.ground.blit(self.rotated_nose, self.rotated_Nase_f)
                else: 
                    pygame.draw.rect(self.ground, "#5870db", segment )
        
        

    def snake_move(self):
        #hier werden die positionen berechnet
        head_x, head_y = self.snake[0].x, self.snake[0].y

        #if head_x % 30 == 0 and head_y % 30 == 0:
        if self.Direction == "LEFT":
            head_x -= self.rectv-27
            if len(self.snake)> 1:
                self.snake[1].x -= 27

        elif self.Direction == "RIGHT":
            head_x += self.rectv-27
            if len(self.snake)> 1:
                self.snake[1].x += 27
        elif self.Direction == "UP":
            head_y -= self.rectv-27
            if len(self.snake)> 1:
                self.snake[1].y += 27
        elif self.Direction == "DOWN":
            head_y += self.rectv-27
            if len(self.snake)> 1:
                self.snake[1].y -= 27
        
        #neue Kopfposition 
        new_head = pygame.Rect(head_x, head_y, self.rectv, self.rectv)
        #entweder append oder so aber wso sieht halts besser aus #
        #gott liebe ich google
        self.snake = [new_head] + self.snake[:-1]

    def borderpatrol(self):
        if (self.snake[0].x < 0 or self.snake[0].x >= self.col_num * self.rectv or 
            self.snake[0].y < 0 or self.snake[0].y >= self.row_num * self.rectv):
            self.running = False

    def direction_angle(self, dir):
        if dir == "LEFT":
            return 270
        elif dir == "RIGHT":
            return 90
        elif dir == "UP":
            return 180
        elif dir == "DOWN":
            return 0

    def make_ground(self):
        for row in range(self.row_num):
            for col in range(self.col_num):
                color = "#b5d567" if (col + row) % 2 == 0 else "#adcf60"
                pygame.draw.rect(self.ground, color, pygame.Rect(col * self.rectv, row * self.rectv, self.rectv, self.rectv))
        
    def spawn(self):
        while self.running:
            self.start = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    self.old_dir = self.Direction

                    if event.key == pygame.K_RIGHT:
                        self.Direction = "RIGHT"
                    elif event.key == pygame.K_LEFT:
                        self.Direction = "LEFT"
                    elif event.key == pygame.K_DOWN:
                        self.Direction = "DOWN"
                    elif event.key == pygame.K_UP:
                        self.Direction = "UP"
                    
                    if self.Direction == self.opossite_dir[self.old_dir]:
                        self.Direction = self.old_dir

            # Update 
            self.make_ground()                                                                         
            self.snake_move()
            berechneter_winkel = self.direction_angle(self.Direction)                
            self.snake_spawn(berechneter_winkel)
            self.spawn_fruit()  

           
            if self.snake[0].colliderect(self.fruit_rect): 
                self.fruit_rect = None
                time.sleep(0.3)
                self.snake.append(pygame.Rect(self.snake[-1].x, self.snake[-1].y, self.rectv, self.rectv))
                self.fruit_counter = 0

            # Update
            pygame.display.flip()
            self.clock.tick(60)

            self.borderpatrol()
            self.end = time.time()

if __name__ == "__main__":
    print("Starte Spiel")
    try:
        menu = Menu()
        menu.options()
        start_zeit = time.time()
        start_game = Ground()
        start_game.spawn()
    except Exception as e:
        print(f"Fehler ->> {e}")
 
 
    print("Spiel beendet")
    ende = time.time()
    print(f"---------------------------------Zeit ={ende - start_zeit}")
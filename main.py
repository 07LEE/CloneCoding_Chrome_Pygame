import pygame
import os
import random

pygame.init()

#Global Constants

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # 화면 설정

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
            pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))] # 달리기

JIMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png")) # 뛰기

DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
            pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))] # 숙이기

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png")),] # 작은 선인장

LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))] # 큰 선인장

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))] # 새

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png")) # 구름 

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png")) # 배경

class Dinosaur():
    X_POS = 80
    Y_POS = 310
    
    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JIMPING
        
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        
        self.step_index = 0
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect() # 충돌을 범위를 만들기 위해서
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump

        if self.step_index >= 10:
            self.step_index = 0
            
        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_jump = True
            self.dino_rum = False
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_jump = False
            self.dino_rum = False
        elif not (self.dino_jump or userInput[pygame.K_Down]):
            self.dino_duck = False
            self.dino_jump = False
            self.dino_rum = True

    def duck(self):
        pass
    
    def run(self):
        self.image = self.run_img[self.step_index//5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1
        
        
    def jump(self):
        pass
    
    def draw(self, SCREEN):
        SCREEN.blit(self.image(self.dino_rect.x, self.dino_rect.y ))
        
        
        
        
        

# 메인 함수 
def main():
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
        SCREEN.fill(255,255,255) # 화면 색상 설정
        
        userInput = pygame.key.gert_pressed() #사용자가 키보드 누르는 행동
        
        player.draw(SCREEN)
        player.update(userInput)

        clock.tick(30) # 프레임 수

main()
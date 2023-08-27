import pygame
import os
import random

pygame.init()

#Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # 화면 설정

RUNNING = [pygame.image.load(os.path.join("Assets\Dino", "DinoRun1.png")),
            pygame.image.load(os.path.join("Assets\Dino", "DinoRun2.png"))] # 달리기

JIMPING = pygame.image.load(os.path.join("Assets\Dino", "DinoJump.png")) # 뛰기

DUCKING = [pygame.image.load(os.path.join("Assets\Dino", "DinoDuck1.png")),
            pygame.image.load(os.path.join("Assets\Dino", "DinoDuck2.png"))] # 숙이기

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets\Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets\Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets\Cactus", "SmallCactus3.png")),] # 작은 선인장

LARGE_CACTUS = [pygame.image.load(os.path.join("Assets\Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets\Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets\Cactus", "LargeCactus3.png"))] # 큰 선인장

BIRD = [pygame.image.load(os.path.join("Assets\Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets\Bird", "Bird2.png"))] # 새

CLOUD = pygame.image.load(os.path.join("Assets\Other", "Cloud.png")) # 구름 

BG = pygame.image.load(os.path.join("Assets\Other", "Track.png")) # 배경

class Dinosaur():
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5
    
    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JIMPING
        
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        
        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
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
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0
            
        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_jump = True
            self.dino_run = False
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_jump = False
            self.dino_run = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_jump = False
            self.dino_run = True

    def duck(self):
        self.image = self.duck_img[0]  # 하나의 이미지 선택
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1
    
    def run(self):
        self.image = self.run_img[self.step_index//5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1
        
    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
            if self.dino_rect.y >= self.Y_POS:  # 점프가 다 끝나면
                self.dino_rect.y = self.Y_POS  # 다시 바닥으로 위치를 맞춤
                self.jump_vel = self.JUMP_VEL
                self.dino_jump = False

    
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud():
    def __init__(self): # 랜덤한 위치에 구름 생성
        self.x = SCREEN_WIDTH + random.randint(800, 1000) 
        self.y = random. randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()
    
    def update(self): 
        self.x -= game_speed
        if self.x < - self.width:
            self.x = SCREEN_WIDTH + random.randint(2600, 3000)
            self.y = random. randint(50, 100)
    
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type): 
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop() # 리스트의 마지막 요소를 반환하고 제거한다.
    
    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle): # Obstacle를 상속 받음
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0 

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


# 메인 함수 
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    death_count = 0
    run = True
    clock = pygame.time.Clock()
    cloud = Cloud()
    player = Dinosaur()
    game_speed = 14
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    
    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render('points: ' + str(points), True, (0,0,0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
        SCREEN.fill((255, 255, 255))  # 흰색으로 화면 채우기
        
        userInput = pygame.key.get_pressed() #사용자가 키보드 누르는 행동
        
        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0 :
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30) # 프레임 수
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))  # 흰색으로 화면 채우기
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0,0,0))
        elif death_count > 0:
            text = font.render("Press any Key to Start", True, (0,0,0))
            score = font.render("Score : " + str(points), True, (0,0,0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)
            SCREEN.blit(score, scoreRect)

        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 140))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()

menu(death_count=0)

main()
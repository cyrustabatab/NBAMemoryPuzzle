import pygame
import random
import os
import time


directory = "logos"

teams = (os.listdir(directory)) * 2



def shuffle():
    random.shuffle(teams)




pygame.init()


font = pygame.font.SysFont("comicsansms",32)
WIDTH,HEIGHT = 1200,800
screen = pygame.display.set_mode((WIDTH,HEIGHT))

clock = pygame.time.Clock()

FPS = 60

logo_1 = pygame.image.load("nba_logo.png").convert_alpha()
logo_1 = pygame.transform.scale(logo_1,(200,600))

logo_2 = pygame.image.load("nba_logo.png").convert_alpha()
logo_2 = pygame.transform.scale(logo_2,(200,600))

pygame.display.set_caption("Memory Puzzle")

LIGHTBLUE = (135,206,250)
BLUE = (0,0,255)
WHITE = (255,255,255)

class Square(pygame.sprite.Sprite):
    
    def __init__(self,x,y,width,height,team):
        
        super().__init__()

        self.blue_square = pygame.Surface((width,height))
        self.blue_square.fill(BLUE) 
        self.team = team
        self.hovered_square = pygame.Surface((width +4,height + 4))    
        self.team_image = pygame.image.load('logos\\' + team).convert_alpha()
        self.team_image = pygame.transform.scale(self.team_image,(width,height))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = BLUE
        self.matched = False
        self.image = self.blue_square        
        self.rect = self.image.get_rect(topleft=(x,y))
        self.selected = False
        self.hovered = False

    
    def contains_point(self,point):
        
        inside = self.rect.collidepoint(point)
        
        result = None
        if (inside and not self.hovered):
            self.switch_images()
            self.selected = True
            return self






    def switch_images(self):
        
        if self.image is self.team_image:
            self.image = self.blue_square
        else:
            self.image = self.team_image

            
           # self.color = LIGHTBLUE
            #self.image.fill(self.color)




rows = 10
cols = 6

square_size = 60






boundary = 4
left_offset = (WIDTH - (square_size * cols + boundary * (cols - 1))) // 2
top_offset = (HEIGHT - (square_size * rows + boundary * (rows - 1))) // 2

def get_squares():

    shuffle()
    squares = pygame.sprite.Group()
    for row in range(rows):
        for col in range(cols):

            square = Square((boundary + square_size) * col  + left_offset,(square_size + boundary) * row + top_offset,square_size,square_size,teams[row * cols + col])

            squares.add(square)
    
    return squares


def check_for_match(selected_squares):


    return selected_squares[0].team == selected_squares[1].team






done = False

squares = get_squares()


current_selected_square = None
selection_count = 0
selected_squares = []
start_time = time.time()
match_text = None
match = False
matches = 0
game_over = False



game_start_time = time.time()

seconds = 0
amount = 2
seconds_text = font.render(str(seconds),True,(0,0,0))

title_text = font.render("NBA LOGO CHALLENGE",True,(0,0,0))
title_rect = title_text.get_rect(center=(WIDTH//2,750))
while not done:
    
    current_time = time.time()

    if not game_over and current_time - game_start_time >= 1:
        seconds += 1
        seconds_text = font.render(str(seconds),True,(0,0,0))
        game_start_time = time.time()


    
    if start_time:

        if current_time - start_time >= amount:

            if game_over:
                squares = get_squares()
                seconds = 0
                seconds_text = font.render(str(seconds),True,(0,0,0))
                matches = 0
                game_over = False
                amount = 2
            else:
                for square in selected_squares:
                    if not match:
                        square.switch_images()
                        square.selected  = False
                    else:
                        square.matched = True
            match = False
            selection_count =0
            start_time = None
            selected_squares.clear()
            match_text = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif selection_count != 2 and event.type == pygame.MOUSEBUTTONDOWN:
            x,y =pygame.mouse.get_pos()
            for square in squares:
                if not square.matched and not square.selected and square.rect.collidepoint((x,y)):
                    selected_squares.append(square)
                    square.selected = True
                    selection_count += 1
                    square.switch_images()
                    if selection_count == 2:
                        if check_for_match(selected_squares):
                            matches += 1
                            text = "MATCH"
                            if matches == 30:
                                game_over = True
                                text = f"You guessed all 30 pairs! in {seconds} seconds!"
                                amount = 5
                            match_text = font.render(text,True,(0,255,0))
                            match_rect = match_text.get_rect(center=(WIDTH//2,20))
                            match = True
                        else:
                            match_text = font.render("NO MATCH",True,(255,0,0))
                            match_rect = match_text.get_rect(center=(WIDTH//2,20))

                        start_time = time.time()

                    

        '''
        elif event.type == pygame.MOUSEMOTION:
            x,y = pygame.mouse.get_pos()
            for square in squares:
                result= square.contains_point((x,y))
                if result is not None:
                    if current_selected_square and current_selected_square is not result:
                        current_selected_square.hovered = False
                        current_selected_square.switch_colors()
                    current_selected_square = result
                    break
        '''



    screen.fill((255,255,255))
    squares.draw(screen)
    

    screen.blit(seconds_text,(1200 - 50,10))
    screen.blit(title_text,title_rect)
    screen.blit(logo_1,(200,20))
    screen.blit(logo_2,(800,20))
    if match_text:
        screen.blit(match_text,match_rect)
    pygame.display.update()
    clock.tick(FPS)

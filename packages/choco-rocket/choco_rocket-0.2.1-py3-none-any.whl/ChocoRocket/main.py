import pygame
import sys
import os
import random
import time
from pygame.locals import *

class Meteor:
    
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

class Player:
    
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

class Chocolate:

    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))


main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_img(name, w, h):
   path = os.path.join(main_dir,"images",name)
   return pygame.transform.scale(pygame.image.load(path), (w,h))


def main():
    pygame.init()
    pygame.font.init()

    # DISPLAY
    WIDTH, HEIGHT = 700, 400
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ChocoRocket")

    # Background
    BG = load_img("bg.png", WIDTH, HEIGHT)

    clock = pygame.time.Clock()

    font = pygame.font.SysFont("comicsans", 40)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    x, y = 0, 200 
    player = Player(x, y, load_img('p1.png', 70, 80))
    meteor = Meteor(660, random.randint(15, 345), load_img('meteor.png', 80, 55))
    choco = Chocolate(660, random.randint(15, 345), load_img('choco.png', 50, 50))

    pause = False

    def button(msg,x,y,w,h,action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()

        font_small = pygame.font.SysFont('courier', 35)
            
        pygame.draw.rect(WIN, BLACK, (x, y, w, h))

        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            message = font_small.render(f"> {msg} <", True, WHITE)
            WIN.blit(message, (x, y))
            
            if click[0] == 1 and action != None:
                if action == 'play':
                    game_loop() 

                elif action == 'quit':
                    pygame.quit()
                    quit()

                elif action == 'play again':
                    player.x, player.y = 0, 200
                    meteor.x, meteor.y = 660, random.randint(15, 345)
                    choco.x, choco.y = 660, random.randint(15, 345)
                    game_loop()

                elif action == 'credits':
                    global run
                    run = True

                    while run:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()

                        WIN.fill(BLACK)
                        new_font = pygame.font.SysFont("courier", 60)
                        title = new_font.render("ChocoRocket", True, RED)
                        msg_font = pygame.font.SysFont("courier", 25)
                        msg = msg_font.render("This Game is a college project made by:", True, WHITE)
                        name = msg_font.render("- Jose Augusto Oliveira Rufino -", True, WHITE)
                        WIN.blit(msg, (55, 150))
                        WIN.blit(name, (90, 210))
                        WIN.blit(title, (165, 0))


                        button("Return", 250, 350, 200, 40,'return')
                
                        pygame.display.update()
                        clock.tick(15)

                elif action == 'controls':
                    run = True

                    while run:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()

                        WIN.fill(BLACK)
                        new_font = pygame.font.SysFont("courier", 60)
                        title = new_font.render("ChocoRocket", True, RED)
                        msg_font = pygame.font.SysFont("courier", 25)
                        title_controls = pygame.font.SysFont("courier", 35).render("Controls:", True, WHITE)
                        msg1 = msg_font.render("- Arrows: UP and DOWN", True, WHITE)
                        msg2 = msg_font.render("- ESC (PAUSE)", True, WHITE)
                        WIN.blit(title_controls, (260, 100))
                        WIN.blit(msg1, (200, 210))
                        WIN.blit(msg2, (200, 240))
                        WIN.blit(title, (165, 0))


                        button("Return", 250, 350, 200, 40,'return')
                
                        pygame.display.update()
                        clock.tick(15)

                elif action == 'return':
                    run = False

                elif action == 'continue':
                    unpause()

                # elif action == 'menu':
                #     global intro
                #     intro = True
                    

        else:
            message = font_small.render(f"< {msg} >", True, WHITE)
            WIN.blit(message, (x, y))

    def unpause():
        global pause
        pause = False

    def paused():
        global pause
        pause = True

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            WIN.fill(BLACK)
            pause_font = pygame.font.SysFont("courier", 60)
            pause_title = pause_font.render("Paused", True, WHITE)
            WIN.blit(pause_title, (230, 30))

            button("Continue", 250, 150, 200, 40, 'continue')
            button("Quit", 250, 210, 200, 40, 'quit')

            pygame.display.update()
            clock.tick(15)


    def game_intro():

        intro = True

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            WIN.fill(BLACK)
            new_font = pygame.font.SysFont("courier", 60)
            title = new_font.render("ChocoRocket", True, RED)
            WIN.blit(title, (165, 0))
            px, py = 110, 55
            WIN.blit(load_img('p1.png', 70, 80), (px, py))
            WIN.blit(load_img('p1.png', 70, 80), (px+420, py))

            button("Start", 250, 130, 200, 40,'play')
            button("Controls", 250, 130+60, 200, 40, 'controls')
            button("Credits", 250, 130+60*2, 200, 40,'credits')
            button("Quit", 250, 130+60*3, 200, 40,'quit')

            pygame.display.update()
            clock.tick(15)


    def redraw_window(lives, score):
        WIN.blit(BG, (0, 0))
        # label score and lives on the screen
        lives_label = font.render(f"Lives: {lives}", 1, (255, 255, 255))
        score_label = font.render(f"Score: {score}", 1, (255, 255, 255))
        
        WIN.blit(lives_label, (10, 10))
        WIN.blit(score_label, (WIDTH - score_label.get_width() - 10, 10))

        # drawing the player
        player.draw(WIN)
        
        # drawing the meteor
        meteor.draw(WIN)

        # drawing the chocolate
        choco.draw(WIN)


        pygame.display.update()

    def colision(name_object):
        # check for vertical collision
        if name_object.x <= (player.x+70):
            # check for horizontal collision
            if 0 < (player.y - name_object.y) < 50 or 0 < (name_object.y - player.y) < 80:
                return True

        return False

    def game_loop():
        lives = 3
        score = 0
        game_over = font.render("Game Over!", True, WHITE)

        vel = 4.5
        vel_meteor = 4.5
        vel_choco = 4

        while True:
            clock.tick(60)
            redraw_window(lives, score)

            score_label = font.render(f"Score: {score}", 1, (255, 255, 255))
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP] and player.y - vel > 20:
                player.y -= vel

            if keys[pygame.K_DOWN] and player.y + vel + 80 < HEIGHT:
                player.y += vel
            
            if keys[pygame.K_ESCAPE]:
                paused()

            meteor.x -= vel_meteor
            choco.x -= vel_choco

            # Meteor
            if meteor.x == player.x or meteor.x < player.x:
                
                # check for collision
                if colision(meteor):
                    lives -= 1

                meteor.y = random.randint(32, 400-55)
                meteor.x = 660
                vel_meteor += 0.25

                if vel_meteor > 14:
                    vel_meteor = 14

            # Chocolate
            if choco.x == player.x or choco.x < player.x:

                # check for collision
                if colision(choco):
                    score += 1
                    # increase player's velocity
                    if score % 11 == 0:
                        vel += 0.4

                choco.y = random.randint(32, 400-50)
                choco.x = 660
                vel_choco += 0.2

                if vel_choco > 12:
                    vel_choco = 12

            if lives == 0:
                time.sleep(1)
                
                final = True
                
                while final:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                    
                    WIN.fill(BLACK)
                    WIN.blit(game_over, (260,180))
                    WIN.blit(score_label, (260,140))
                    button("Play Again", 50, 350, 350, 40,'play again')
                    button("Quit", 450, 350, 200, 40,'quit')

                    pygame.display.update()

    
    game_intro()

if __name__ == "__main__":
    main()

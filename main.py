import pygame
import sys
from random import randint, uniform

black = (0, 0, 0)
white = (255, 255, 255)
WIDTH = 920
HEIGHT = 720
step = 15
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
window = screen.get_rect()
pygame.display.set_caption('PyPong!')

box1 = pygame.Rect(0, 0, 30, 30)
box1.center = window.center
box2 = pygame.Rect(0, 0, 30, 60)
box2.midleft = window.midleft

ball_speed = [-1, 0]
score = [0, 0]
pygame.key.set_repeat(50, 50)
fps = pygame.time.Clock()

menu = True
singleplayer = False
multiplayer = False

left_paddle = pygame.Rect(0, 0, 15, 120)
left_paddle.midleft = window.midleft
right_paddle = pygame.Rect(0, 0, 15, 120)
right_paddle.midright = window.midright
ball = pygame.Rect(0, 0, 20, 20)
ball.center = window.center


largefont = pygame.font.Font('freesansbold.ttf', 50)
smallfont = pygame.font.Font('freesansbold.ttf', 30)


def show_menu():
    global menu, multiplayer, singleplayer

    # title
    maintext = largefont.render("PyPong!", True, white)
    maintext_rect = maintext.get_rect()
    maintext_rect.center = (WIDTH/2, HEIGHT/2 - 200)
    screen.blit(maintext, maintext_rect)

    # singleplayer
    singletext = smallfont.render("Singleplayer", True, black)
    singletext_rect = singletext.get_rect()
    singletext_rect.center = (WIDTH/2, HEIGHT/2 - 50)
    pygame.draw.rect(screen, white, singletext_rect)
    screen.blit(singletext, singletext_rect)

    # multiplayer
    multitext = smallfont.render("Multiplayer", True, black)
    multitext_rect = multitext.get_rect()
    multitext_rect.center = (WIDTH/2, HEIGHT/2 + 20)

    pygame.draw.rect(screen, white, multitext_rect)
    screen.blit(multitext, multitext_rect)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()

            if singletext_rect.collidepoint(mouse):
                singleplayer = True
                menu = False
            if multitext_rect.collidepoint(mouse):
                multiplayer = True
                menu = False

    pygame.display.flip()


def draw_field():
    pygame.draw.line(screen, white, (WIDTH/2, 0), (WIDTH/2, HEIGHT))


def draw_paddles():
    pygame.draw.rect(screen, white, left_paddle)
    pygame.draw.rect(screen, white, right_paddle)


def draw_ball():
    pygame.draw.rect(screen, white, ball)


def keep_paddles():
    if left_paddle.top < window.top:
        left_paddle.top = window.top
    if left_paddle.bottom > window.bottom:
        left_paddle.bottom = window.bottom
    if right_paddle.top < window.top:
        right_paddle.top = window.top
    if right_paddle.bottom > window.bottom:
        right_paddle.bottom = window.bottom


def ball_collide():
    global ball_speed
    # top and bottom collision
    if ball.top < window.top or ball.bottom > window.bottom:
        ball_speed[1] = -ball_speed[1]
        ball_speed[0] = ball_speed[0] * 1.1
        ball_speed[1] = ball_speed[1] * 1.1

    # paddle collision
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed[0] = -ball_speed[0]
        ball_speed[1] = randint(-2, 2)
        ball_speed[0] = ball_speed[0] * 1.1
        ball_speed[1] = ball_speed[1] * 1.1

    # right goal
    if ball.left < window.left:
        ball_speed = [-1, 0]
        ball.center = window.center
        score[1] = score[1] + 1
        left_paddle.midleft = window.midleft
        right_paddle.midright = window.midright

    # left goal
    if ball.right > window.right:
        ball_speed = [1, 0]
        ball.center = window.center
        score[0] = score[0] + 1
        left_paddle.midleft = window.midleft
        right_paddle.midright = window.midright


def score_text():
    leftscore = largefont.render(str(score[0]), True, white)
    leftscore_text = leftscore.get_rect()
    leftscore_text.center = (WIDTH/4, HEIGHT/8)

    screen.blit(leftscore, leftscore_text)

    rightscore = largefont.render(str(score[1]), True, white)
    rightscore_text = rightscore.get_rect()
    rightscore_text.center = (3 * WIDTH/4, HEIGHT/8)

    screen.blit(rightscore, rightscore_text)


def restart():
    global score, left_paddle, right_paddle
    left_paddle.midleft = window.midleft
    right_paddle.midright = window.midright
    screen.fill(black)
    score = [0, 0]
    left_paddle.midleft = window.midleft
    right_paddle.midright = window.midright


if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                menu = True
                multiplayer = False
                singleplayer = False
                restart()

            if not menu:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        left_paddle = left_paddle.move(0, -step)
                    if event.key == pygame.K_DOWN:
                        left_paddle = left_paddle.move(0, step)

                    if multiplayer:
                        if event.key == pygame.K_w:
                            right_paddle = right_paddle.move(0, -step)
                        if event.key == pygame.K_s:
                            right_paddle = right_paddle.move(0, step)

        if menu:
            show_menu()
        else:
            if singleplayer:
                if ball_speed[1] > 0:
                    pos = uniform(1, ball_speed[1])
                    right_paddle = right_paddle.move(0, pos)
                elif ball_speed[1] < 0:
                    pos = uniform(ball_speed[1], -1)
                    right_paddle = right_paddle.move(0, pos)

            ball = ball.move(ball_speed)
            screen.fill(black)

            draw_field()
            draw_ball()
            draw_paddles()
            keep_paddles()
            ball_collide()
            score_text()

            pygame.display.flip()
            fps.tick(260)

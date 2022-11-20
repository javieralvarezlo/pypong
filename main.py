import pygame
import sys

black = (0, 0, 0)
white = (255, 255, 255)
WIDTH = 920
HEIGHT = 720
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
window = screen.get_rect()
pygame.display.set_caption('PyPong!')

box1 = pygame.Rect(0, 0, 30, 30)
box1.center = window.center
box2 = pygame.Rect(0, 0, 30, 60)
box2.midleft = window.midleft

vec = [1, 0]
pygame.key.set_repeat(50, 50)
fps = pygame.time.Clock()

menu = True
singleplayer = False
multiplayer = False


def show_menu():
    global menu, singleplayer, multiplayer
    largefont = pygame.font.Font('freesansbold.ttf', 50)
    smallfont = pygame.font.Font('freesansbold.ttf', 30)

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
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()

            if singletext_rect.collidepoint(mouse):
                singleplayer = True
                menu = False
            if multitext_rect.collidepoint(mouse):
                multiplayer = True
                menu = False

    pygame.display.flip()


if __name__ == "__main__":
    while True:
        if menu:
            show_menu()

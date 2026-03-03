import pygame
import sys
import pygame as pg
from movement import Player
from projectiles import Arrow

pygame.init()

WIDTH, HEIGHT = 1200, 750  # sæt størrelse på mainwindow
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Topdown Shooter")

clock = pygame.time.Clock() # load tiden

player = Player(WIDTH // 2, HEIGHT // 2) # sæt player midt i mainwindow

arrows = [] # sæt pilene som en liste

fighter_anim = []
for i in range(4):
    img = pg.image.load(f"Images/Fighter_anim{i}.png")
    fighter_anim.append(img)

frame_counter = 0



running = True
while running:
    clock.tick(60) # sæt til 60 ticks i sekundet

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # gør at programmet kan slukke

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # starter når man trykker space
                mouse_pos = pygame.mouse.get_pos() # få lokationen af musen til at sigte pilene

                
                arrow = Arrow( 
                    player.position.x,
                    player.position.y,
                    speed=12,
                    size=5,
                    damage=25,
                    target_pos=mouse_pos # laver et objekt fra arrow-klassen og sigter mod musen
                )

                arrows.append(arrow) # skubber det nye objekt i listen til pile

    
    player.handle_input()
    player.constrain_to_screen(WIDTH, HEIGHT) # gør at spilleren ikke kan bevæge sig ud af mainwindow

   
    for arrow in arrows[:]:
        arrow.update(WIDTH, HEIGHT)
        if not arrow.alive:
            arrows.remove(arrow) # fjerner pile når de er ude af vinduet

    
    screen.fill((255, 255, 255)) # gør vinduet vidt (skal erstattes med billede)

    frame = (frame_counter // 6) % len(fighter_anim)

    img = fighter_anim[frame]
    x = int(player.position.x - img.get_width() / 2)
    y = int(player.position.y - img.get_height() / 2)

    screen.blit(img, (x, y))

    player.draw(screen) # tegner spilleren på skærmen

    for arrow in arrows:
        arrow.draw(screen) # tegner pilene fra listen

    pygame.display.flip()
    frame_counter += 1

pygame.quit()
sys.exit()

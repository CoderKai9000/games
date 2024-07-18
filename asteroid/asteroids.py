import pygame
from random import randint

pygame.init()
pygame.font.init()

WIDTH = 1200
HEIGHT = 900
FPS = 60

def update_ship_pos(ship_rect, ship_inputs, ship_speed):
    ship_vel = (ship_inputs["right"] - ship_inputs["left"])
    new_x = ship_rect.x + ship_vel * ship_speed
    if 0 <= new_x <= WIDTH - ship_rect.width:
        ship_rect.x = new_x
    elif new_x < 0:
        ship_rect.x = 0
    elif new_x > WIDTH - ship_rect.width:
        ship_rect.x = WIDTH - ship_rect.width


screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()

# screens:
window = pygame.Surface((WIDTH,HEIGHT))
# ship
ship = pygame.Surface((20,20), pygame.SRCALPHA)
pygame.draw.rect(ship,(255,255,255),(0,0,20,20))
ship_rect = ship.get_rect(midbottom=(WIDTH//2,HEIGHT-20))
ship_inputs = {"left": False, "right":False}
ship_speed = 8
total_lives = 5

# bullet
bul = pygame.Surface((5,10), pygame.SRCALPHA)
pygame.draw.rect(bul,(0,0,255),(0,0,5,10))
bul_rect = bul.get_rect(midtop=ship_rect.midtop)
bul_vel = [0,2]
bul_speed = 5
bul_list = []
bul_spawn_delay = 0.3

# asteroid
aster_radius = 15
aster = pygame.Surface((aster_radius*2, aster_radius*2), pygame.SRCALPHA)
aster.fill((0, 0, 0, 0))
pygame.draw.circle(aster, (255, 0, 0), (aster_radius, aster_radius), aster_radius)
aster_rect = aster.get_rect(center=(WIDTH // 2, HEIGHT // 2))
aster_speed = 3
aster_list = []
aster_spawn_delay = 1

# score
font = pygame.font.SysFont(None, 48)
hit_count = 0
miss_count = 0
score_text = font.render(f"Score:{hit_count}", True, (0,0,0))
score_rect = score_text.get_rect(topleft=(10,10))
score_bg_surface = pygame.Surface((score_rect.width, score_rect.height))
score_bg_surface.fill((0,255,0))
miss_text = font.render(f"Lives Left:{total_lives-miss_count}", True, (0,0,0))
miss_rect = miss_text.get_rect(topright=(WIDTH-10,10))
miss_bg_surface = pygame.Surface((miss_rect.width, miss_rect.height))
miss_bg_surface.fill((0,255,0))

# screens:
    # game over
go_screen = pygame.Surface((WIDTH, HEIGHT))
gofont = pygame.font.SysFont(None, 120)
go_text = gofont.render("[GAME OVER]", True, (255,255,255))
go_rect = go_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    # restart text
refont = pygame.font.SysFont(None, 40)
re_text = refont.render("[R] to restart", True, (255,255,255))
re_rect = re_text.get_rect(center = (int(0.75*WIDTH),(go_rect.y+HEIGHT)//2))
    # home screen
home_screen = pygame.Surface((WIDTH, HEIGHT))
wel_text = gofont.render("Asteroids!!!", True, (255,255,255))
wel_rect = wel_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    # start instructions:
text = "[\u2191] to fire\n[\u2190] to go left\n[\u2192] ot go right\ndestroy as many asteroids as possible\ngood luck!!!\nPress [E] to begin"
lines = text.split('\n')
stfont = pygame.font.SysFont(None, 30)
st_text = stfont.render("", True, (255,255,255))
st_rect = st_text.get_rect(center = (WIDTH//2,(wel_rect.y+HEIGHT)//2))
aster_timer = 0
bul_timer = 0

run = True
game_state = "home"

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if bul_timer >= FPS*bul_spawn_delay:
                    new_bul_rect = bul.get_rect(midtop=ship_rect.midtop)
                    bul_list.append([new_bul_rect,1])
                    bul_timer = 0
            if event.key == pygame.K_LEFT:
                ship_inputs["left"] = True
            if event.key == pygame.K_RIGHT:
                ship_inputs["right"] = True
            if game_state == "game over" and event.key == pygame.K_r:
                hit_count = 0
                miss_count = 0
                bul_list = []
                aster_list = []
                ship_rect.x = WIDTH//2
                game_state = "play"
            if game_state == "home" and event.key == pygame.K_e:
                game_state = "play"

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                ship_inputs["left"] = False
            if event.key == pygame.K_RIGHT:
                ship_inputs["right"] = False

    if game_state == "home":
        screen.blit(wel_text, wel_rect)
        inst_y=(wel_rect.y+HEIGHT)//2
        for line in lines:
            inst_text = stfont.render(line, True, (255,255,255))
            inst_rect = inst_text.get_rect(midtop = (WIDTH//2,inst_y))
            screen.blit(inst_text, inst_rect)
            inst_y+=font.get_linesize()

    if game_state == "play":
        bul_timer+=1
        aster_timer+=1
        screen.blit(window,(0,0))
        if total_lives-miss_count <= 0:
            game_state = "game over"
            continue

        # Ship
        screen.blit(ship,ship_rect)
        update_ship_pos(ship_rect, ship_inputs, ship_speed)

        # Bullets
        for rect in bul_list:
            if rect[0].bottom < 0:
                bul_list.pop(0)
            if rect[1] == 1:
                rect[0].y-=bul_speed
                screen.blit(bul, rect[0])

        # Asteroids
        if aster_timer >= FPS*aster_spawn_delay:
            spawn_loc = randint(aster_radius+5, WIDTH-aster_radius-5)
            new_aster_rect = aster.get_rect(center=(spawn_loc, -aster_radius))
            aster_list.append([new_aster_rect,1])
            aster_timer = 0

        for rect in aster_list:
            if rect[0].top == HEIGHT:
                miss_count+=1
                aster_list.pop(0)
            for bul_rect in bul_list:
                if rect[0].colliderect(bul_rect[0]) and rect[1] == 1 and bul_rect[1] == 1:
                    rect[1] = 0
                    bul_rect[1] = 0
                    hit_count+=1
            if rect[1] == 1:
                rect[0].y+=aster_speed
                screen.blit(aster, rect[0])

        # Score
        score_text = font.render(f"Score:{hit_count}", True, (0,0,0))
        score_rect = score_text.get_rect(topleft=(10,10))
        screen.blit(score_bg_surface,score_rect)
        screen.blit(score_text, score_rect)
        miss_text = font.render(f"Lives Left:{total_lives-miss_count}", True, (0,0,0))
        miss_rect = miss_text.get_rect(topright=(WIDTH-10,10))
        screen.blit(miss_bg_surface,miss_rect)
        screen.blit(miss_text, miss_rect)
    elif game_state == "game over":
        screen.blit(go_screen, (0,0))
        screen.blit(go_text,go_rect)
        screen.blit(re_text,re_rect)
        fsc_text = refont.render(f"Your Score:{hit_count}", True, (255,255,255))
        fsc_rect = fsc_text.get_rect(center = (int(0.25*WIDTH),(go_rect.y+HEIGHT)//2))
        screen.blit(fsc_text,fsc_rect)
    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()

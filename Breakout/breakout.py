import pygame

pygame.init()
pygame.font.init()

WIDTH = 1200
HEIGHT = 900
FPS = 60

def update_player_pos(player_rect,player_inputs,player_speed):
    player_vel = (player_inputs["right"] - player_inputs["left"])
    new_x = player_rect.x + player_vel * player_speed
    if 0 <= new_x <= WIDTH - player_rect.width:
        player_rect.x = new_x
    elif new_x < 0:
        player_rect.x = 0
    elif new_x > WIDTH - player_rect.width:
        player_rect.x = WIDTH - player_rect.width

def horiz_coll(ball_rect):
    if ball_rect.left <= 0 or ball_rect.right >= WIDTH:
        return 1
    else:
        return 0

def ciel_coll(ball_rect):
    if ball_rect.top <= 0:
        return 1
    else:
        return 0
def main():
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Breakout")
    clock = pygame.time.Clock()

    # screens:
    window = pygame.Surface((WIDTH,HEIGHT))
    font = pygame.font.SysFont(None, 48)
    go_screen = pygame.Surface((WIDTH, HEIGHT))
    gofont = pygame.font.SysFont(None, 120)
    go_text = gofont.render("[GAME OVER]", True, (255,255,255))
    go_rect = go_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    vic_text = gofont.render("[YOU WIN]", True, (255,255,255))
    vic_rect = vic_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        # restart text
    refont = pygame.font.SysFont(None, 40)
    re_text = refont.render("[R] to restart", True, (255,255,255))
    re_rect = re_text.get_rect(center = (int(0.75*WIDTH),(go_rect.y+HEIGHT)//2))
        # home screen
    home_screen = pygame.Surface((WIDTH, HEIGHT))
    wel_text = gofont.render("BREAKOUT", True, (255,255,255))
    wel_rect = wel_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        # start instructions:
    text = "[\u2190]Left\n[\u2192]Right\nBreak all the Bricks to win!!!\nPress [E] to play"
    lines = text.split('\n')
    stfont = pygame.font.SysFont(None, 30)
    st_text = stfont.render("", True, (255,255,255))
    st_rect = st_text.get_rect(center = (WIDTH//2,(wel_rect.y+HEIGHT)//2))

    hit_count = 0

    # player:
    player = pygame.Surface((80,10), pygame.SRCALPHA)
    pygame.draw.rect(player, (255,255,255), (0,0,80,10))
    player_rect = player.get_rect(midbottom = (WIDTH//2, HEIGHT-15))
    player_inputs = {"left":False, "right":False}
    player_speed = 8

        # ball:
    #ball status
    ball_inputs = {'left':False, 'right':False, 'up':False, 'down':False}
    ball_velocity = [0,0]
    ball_x = 400
    ball_y = 200
    ball_speed = 3
    ball_radius = 10
    x_speed = 5
    y_speed = -5

    #ball object
    ball = pygame.Surface((ball_radius*2, ball_radius*2), pygame.SRCALPHA)
    ball.fill((0, 0, 0, 0))
    pygame.draw.circle(ball, (255, 0, 0), (ball_radius, ball_radius), ball_radius)
    ball_rect = ball.get_rect(midbottom=player_rect.midtop)

        # brick
    # brick object
    brick_list = []
    brx = 5
    bry = 5
    brwdth = 50
    brick = pygame.Surface((50, 20), pygame.SRCALPHA)
    pygame.draw.rect(brick,(255,0,0), (0,0,50,20))
    color_list = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]
    for i in range(0,20):
        for j in range(0,23):
            brick_rect = brick.get_rect(topleft = (brx,50+bry))
            brick_list.append([brick_rect, 1, color_list[i%6]])
            brx+=53
        brx = 5
        bry+=25

    run = True
    game_state = "home"
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_inputs["left"] = True
                if event.key == pygame.K_RIGHT:
                    player_inputs["right"] = True
                if game_state == "game over" and event.key == pygame.K_r:
                    player_rect.x = WIDTH//2
                    ball_rect.midbottom = player_rect.midtop
                    for brk in brick_list:
                        brk[1] = 1
                    game_state = "home"
                if game_state == "home" and event.key == pygame.K_e:
                    game_state = "play"
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player_inputs["left"] = False
                if event.key == pygame.K_RIGHT:
                    player_inputs["right"] = False

        if game_state == "home":
            screen.blit(window, (0,0))
            screen.blit(wel_text, wel_rect)
            inst_y=(wel_rect.y+HEIGHT)//2
            for line in lines:
                inst_text = stfont.render(line, True, (255,255,255))
                inst_rect = inst_text.get_rect(midtop = (WIDTH//2,inst_y))
                screen.blit(inst_text, inst_rect)
                inst_y+=font.get_linesize()
        elif game_state == "play":
            screen.blit(window, (0,0))
            score_text = font.render(f"Score:{hit_count}", True, (0,0,0))
            score_rect = score_text.get_rect(topleft=(10,10))
            score_bg_surface = pygame.Surface((score_rect.width, score_rect.height))
            score_bg_surface.fill((0,255,0))
            screen.blit(score_bg_surface,score_rect)
            screen.blit(score_text, score_rect)
            update_player_pos(player_rect,player_inputs,player_speed)
            if horiz_coll(ball_rect):
                x_speed*=-1
            if ciel_coll(ball_rect) or ball_rect.colliderect(player_rect):
                y_speed*=-1
            screen.blit(player, player_rect)
            ball_rect.x+=x_speed
            ball_rect.y+=y_speed
            screen.blit(ball,ball_rect)
            if ball_rect.top >= HEIGHT:
                game_state = "game over"
            for brk in brick_list:
                if brk[1] == 1:
                    color = brk[2]
                    pygame.draw.rect(brick, color, (0,0,50,20))
                    screen.blit(brick, brk[0])
            for brk in brick_list:
                if ball_rect.colliderect(brk[0]) and brk[1] == 1:
                    if (ball_rect.left < brk[0].right and ball_rect.right > brk[0].right) or (ball_rect.right > brk[0].left and ball_rect.left < brk[0].left):
                        x_speed*=-1
                        brk[1] = 0
                        hit_count+=1
                    elif (ball_rect.top < brk[0].bottom and ball_rect.bottom > brk[0].bottom) or (ball_rect.bottom > brk[0].top and ball_rect.top < brk[0].top):
                        y_speed*=-1
                        brk[1] = 0
                        hit_count+=1
            if hit_count == 460:
                game_state = "victory"

        elif game_state == "game over":
            screen.blit(window,(0,0))
            screen.blit(go_screen, (0,0))
            screen.blit(go_text,go_rect)
            screen.blit(re_text,re_rect)
            fsc_text = refont.render(f"Your Score:{hit_count}", True, (255,255,255))
            fsc_rect = fsc_text.get_rect(center = (int(0.25*WIDTH),(go_rect.y+HEIGHT)//2))
            screen.blit(fsc_text,fsc_rect)
        elif game_state == "victory":
            screen.blit(go_screen, (0,0))
            screen.blit(vic_text,vic_rect)
            screen.blit(re_text,re_rect)
            fsc_text = refont.render(f"Your Score:{hit_count}", True, (255,255,255))
            fsc_rect = fsc_text.get_rect(center = (int(0.25*WIDTH),(vic_rect.y+HEIGHT)//2))
            screen.blit(fsc_text,fsc_rect)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()

import pygame
from random import randint
WIDTH = 800
HEIGHT = 400
FPS = 60

def update_pos(p1_rect, p2_rect, p1_vel, p2_vel, ball_speed, p1_inputs, p2_inputs,player_speed):
    p1_vel = (p1_inputs['down']-p1_inputs['up'])
    p2_vel = (p2_inputs['down']-p2_inputs['up'])
    if p1_rect.top >= 0 and p1_rect.bottom <= HEIGHT:
        p1_rect.y+=p1_vel*player_speed
    if p2_rect.top >= 0 and p2_rect.bottom <= HEIGHT:
        p2_rect.y+=p2_vel*player_speed

def vert_coll(ball_rect):
    if ball_rect.top <= 0 or ball_rect.bottom >= HEIGHT:
        return True
    else:
        return False

def horiz_coll(ball_rect, p1_rect, p2_rect):
    if (ball_rect.left <= 0 or ball_rect.right >= WIDTH) and (ball_rect.colliderect(p1_rect) or ball_rect.colliderect(p2_rect)):
        return 1
    elif ball_rect.right >= WIDTH:
        return 2 # p1 wins
    elif ball_rect.left <= 0:
        return 3 # p2 wins
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("testgame")
    clock = pygame.time.Clock()

    ##  PLAYER1
    #ball status
    ball_inputs = {'left':False, 'right':False, 'up':False, 'down':False}
    ball_velocity = [0,0]
    ball_x = 400
    ball_y = 200
    ball_speed = 3
    ball_radius = 10

    #ball object
    ball = pygame.Surface((ball_radius*2, ball_radius*2), pygame.SRCALPHA)
    ball.fill((0, 0, 0, 0))
    pygame.draw.circle(ball, (255, 0, 0), (ball_radius, ball_radius), ball_radius)
    ball_rect = ball.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Player 1 object
    p1 = pygame.Surface((5, 50), pygame.SRCALPHA)
    p1.fill((0, 0, 0, 0))
    p1_inputs = {'up':False, 'down':False}
    pygame.draw.rect(p1, (255, 255, 255), (0, 0, 5, 50))
    p1_rect = p1.get_rect(midleft=(0, HEIGHT // 2))
    p1_vel = 0

    # Player 2 object
    p2 = pygame.Surface((5, 50), pygame.SRCALPHA)
    p2.fill((0, 0, 0, 0))
    p2_inputs = {'up':False, 'down':False}
    pygame.draw.rect(p2, (255, 255, 255), (0, 0, 5, 50))
    p2_rect = p2.get_rect(midright=(WIDTH, HEIGHT // 2))
    p2_vel = 0

    player_speed = 5

    # test

    x_speed = 2
    y_speed = 2

    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if p1_rect.top >= 0:
                        p1_inputs['up'] = True
                elif event.key == pygame.K_s:
                    if p1_rect.bottom <= HEIGHT:
                        p1_inputs['down'] = True
                elif event.key == pygame.K_UP:
                    if p2_rect.top >= 0:
                        p2_inputs['up'] = True
                elif event.key == pygame.K_DOWN:
                    if p2_rect.bottom <= HEIGHT:
                        p2_inputs['down'] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    if p1_rect.top >= 0:
                        p1_inputs['up'] = False
                elif event.key == pygame.K_s:
                    if p1_rect.bottom <= HEIGHT:
                        p1_inputs['down'] = False
                elif event.key == pygame.K_UP:
                    if p2_rect.top >= 0:
                        p2_inputs['up'] = False
                elif event.key == pygame.K_DOWN:
                    if p2_rect.bottom <= HEIGHT:
                        p2_inputs['down'] = False

        screen.fill((0,0,0))
        screen.blit(ball, ball_rect)
        screen.blit(p1, p1_rect)
        screen.blit(p2, p2_rect)
        randval = randint(500,1500) / 1000
        if vert_coll(ball_rect):
            y_speed*=-1*randval

        match horiz_coll(ball_rect, p1_rect, p2_rect):
            case 1:
                x_speed*=-1*randval
            case 2:
                print("P1 wins")
                run = False
            case 3:
                print("P2 wins")
                run = False

        ball_rect.x+=int(x_speed*ball_speed)
        ball_rect.y+=int(y_speed*ball_speed)
        update_pos(p1_rect, p2_rect, p1_vel, p2_vel, ball_speed, p1_inputs, p2_inputs,player_speed)
        pygame.display.flip()

if __name__ == "__main__":
    main()

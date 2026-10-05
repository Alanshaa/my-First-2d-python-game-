import pygame
import random
import math

pygame.init()

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2 KM Road Challenge")

clock = pygame.time.Clock()


SKY = (100, 180, 240)
GRASS = (40, 130, 50)
ROAD = (65, 65, 65)
ROAD_EDGE = (220, 220, 220)
WHITE = (255, 255, 255)
RED = (220, 40, 40)
BLUE = (30, 120, 255)
YELLOW = (255, 220, 0)
BLACK = (20, 20, 20)


MAX_DISTANCE = 2000      
distance = 0
speed = 0

player_x = WIDTH // 2
player_y = HEIGHT - 130

player_width = 45
player_height = 75

road_width = 300

game_state = "playing"

road_center = WIDTH // 2

obstacles = []

trees = []



def reset_game():
    global distance
    global speed
    global player_x
    global road_center
    global obstacles
    global trees
    global game_state

    distance = 0
    speed = 0

    player_x = WIDTH // 2
    road_center = WIDTH // 2

    obstacles = []
    trees = []

    game_state = "playing"



def create_tree(y):
    side = random.choice([-1, 1])

    x = road_center + side * random.randint(
        road_width // 2 + 50,
        road_width // 2 + 180
    )

    trees.append([x, y])



def create_obstacle(y):

    x = road_center + random.randint(
        -road_width // 2 + 30,
        road_width // 2 - 70
    )

    obstacles.append(
        pygame.Rect(x, y, 45, 45)
    )


for y in range(-100, HEIGHT, 120):
    create_tree(y)

for y in range(-300, HEIGHT, 350):
    create_obstacle(y)



running = True

while running:

    dt = clock.tick(60) / 1000


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                reset_game()


    if game_state == "playing":

        keys = pygame.key.get_pressed()


        if keys[pygame.K_UP] or keys[pygame.K_w]:

            speed += 0.08

        else:

            speed -= 0.04

        speed = max(2, min(speed, 9))

        # Left / Right movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:

            player_x -= 300 * dt

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:

            player_x += 300 * dt


        road_center += math.sin(distance / 150) * 0.15

        road_left = road_center - road_width // 2
        road_right = road_center + road_width // 2



        player_left = player_x - player_width / 2
        player_right = player_x + player_width / 2

        if player_left < road_left or player_right > road_right:

            game_state = "lost"


        distance += speed * dt * 2

        if distance >= MAX_DISTANCE:

            distance = MAX_DISTANCE
            game_state = "won"


        for obstacle in obstacles:

            obstacle.y += speed * 2


        
        obstacles = [
            obstacle for obstacle in obstacles
            if obstacle.y < HEIGHT + 100
        ]


        # Generate new obstacles
        if len(obstacles) < 6:

            create_obstacle(
                random.randint(-400, -50)
            )



        for tree in trees:

            tree[1] += speed * 2


        trees = [
            tree for tree in trees
            if tree[1] < HEIGHT + 100
        ]


        # Generate new trees
        if len(trees) < 15:

            create_tree(
                random.randint(-500, -50)
            )

        player_rect = pygame.Rect(
            player_x - player_width // 2,
            player_y,
            player_width,
            player_height
        )


        for obstacle in obstacles:

            if player_rect.colliderect(obstacle):

                game_state = "lost"


    screen.fill(SKY)

    pygame.draw.rect(
        screen,
        GRASS,
        (0, HEIGHT // 3, WIDTH, HEIGHT)
    )



    road_left = road_center - road_width // 2

    pygame.draw.rect(
        screen,
        ROAD,
        (
            road_left,
            0,
            road_width,
            HEIGHT
        )
    )


    # Road edges
    pygame.draw.line(
        screen,
        ROAD_EDGE,
        (road_left, 0),
        (road_left, HEIGHT),
        6
    )

    pygame.draw.line(
        screen,
        ROAD_EDGE,
        (road_left + road_width, 0),
        (road_left + road_width, HEIGHT),
        6
    )



    for y in range(-50, HEIGHT, 80):

        pygame.draw.rect(
            screen,
            WHITE,
            (
                int(road_center - 4),
                y,
                8,
                40
            )
        )


    for tree in trees:

        x, y = tree

        # trunk
        pygame.draw.rect(
            screen,
            (100, 60, 25),
            (x - 7, y + 25, 14, 35)
        )

        # leaves
        pygame.draw.circle(
            screen,
            (20, 100, 30),
            (x, y + 20),
            25
        )


    for obstacle in obstacles:

        pygame.draw.rect(
            screen,
            RED,
            obstacle,
            border_radius=8
        )

        pygame.draw.line(
            screen,
            YELLOW,
            obstacle.topleft,
            obstacle.bottomright,
            6
        )



    player_rect = pygame.Rect(
        player_x - player_width // 2,
        player_y,
        player_width,
        player_height
    )

    # Car body
    pygame.draw.rect(
        screen,
        BLUE,
        player_rect,
        border_radius=10
    )

    # Windows
    pygame.draw.rect(
        screen,
        (40, 40, 60),
        (
            player_rect.x + 8,
            player_rect.y + 10,
            player_width - 16,
            25
        ),
        border_radius=5
    )

    # Wheels
    pygame.draw.rect(
        screen,
        BLACK,
        (
            player_rect.x - 6,
            player_rect.y + 10,
            8,
            22
        )
    )

    pygame.draw.rect(
        screen,
        BLACK,
        (
            player_rect.right - 2,
            player_rect.y + 10,
            8,
            22
        )
    )

    pygame.draw.rect(
        screen,
        BLACK,
        (
            player_rect.x - 6,
            player_rect.bottom - 30,
            8,
            22
        )
    )

    pygame.draw.rect(
        screen,
        BLACK,
        (
            player_rect.right - 2,
            player_rect.bottom - 30,
            8,
            22
        )
    )


    font = pygame.font.Font(None, 32)

    distance_text = font.render(
        f"Distance: {int(distance)} / 2000 m",
        True,
        WHITE
    )

    speed_text = font.render(
        f"Speed: {int(speed * 10)} km/h",
        True,
        WHITE
    )

    screen.blit(
        distance_text,
        (20, 20)
    )

    screen.blit(
        speed_text,
        (20, 55)
    )



    if game_state == "won":

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 160))

        screen.blit(
            overlay,
            (0, 0)
        )

        big_font = pygame.font.Font(
            None,
            90
        )

        win_text = big_font.render(
            "YOU WIN!",
            True,
            YELLOW
        )

        screen.blit(
            win_text,
            win_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 - 40)
            )
        )

        small_font = pygame.font.Font(
            None,
            35
        )

        restart = small_font.render(
            "Press SPACE to try again",
            True,
            WHITE
        )

        screen.blit(
            restart,
            restart.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 50)
            )
        )

    if game_state == "lost":

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 170))

        screen.blit(
            overlay,
            (0, 0)
        )

        big_font = pygame.font.Font(
            None,
            90
        )

        lose_text = big_font.render(
            "YOU LOSE!",
            True,
            RED
        )

        screen.blit(
            lose_text,
            lose_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 - 40)
            )
        )

        small_font = pygame.font.Font(
            None,
            35
        )

        restart = small_font.render(
            "Press SPACE to try again",
            True,
            WHITE
        )

        screen.blit(
            restart,
            restart.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 50)
            )
        )


    pygame.display.flip()


pygame.quit()
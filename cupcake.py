import pygame
import sys
import random
import os

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cat Fish Collector")

clock = pygame.time.Clock()


BACKGROUND = (135, 206, 235)
BLUE = (0, 122, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 180, 0)


current_folder = os.path.dirname(__file__)
main_folder = os.path.dirname(current_folder)

cat_path = os.path.join(main_folder, "cat.png")
fish_path = os.path.join(main_folder, "fish.webp")


cat_image = pygame.image.load(cat_path).convert_alpha()

# Remove white background around cat
cat_image.set_colorkey((255, 255, 255))

cat_image = pygame.transform.scale(cat_image, (50, 50))


fish_image = pygame.image.load(fish_path).convert_alpha()
fish_image = pygame.transform.scale(fish_image, (35, 25))


player_rect = pygame.Rect(380, 100, 30, 30)

player_vel_x = 0
player_vel_y = 0

player_speed = 6


GRAVITY = 0.8
JUMP_STRENGTH = -15

is_grounded = False


platforms = [
    pygame.Rect(0, 550, 800, 50),
    pygame.Rect(100, 400, 250, 20),
    pygame.Rect(450, 300, 250, 20)
]


fish = []


def make_fish():

    x = random.randint(40, 740)

    # Fish spawn lower on the screen
    y = random.randint(280, 510)

    return pygame.Rect(x, y, 35, 25)


for i in range(10):
    fish.append(make_fish())


fish_score = 0


font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 60)


last_fish_time = pygame.time.get_ticks()


game_over = False
win = False


running = True


while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r and (game_over or win):

                player_rect.x = 380
                player_rect.y = 100

                player_vel_x = 0
                player_vel_y = 0

                fish_score = 0

                fish.clear()

                for i in range(10):
                    fish.append(make_fish())

                last_fish_time = pygame.time.get_ticks()

                game_over = False
                win = False


    if not game_over and not win:

        keys = pygame.key.get_pressed()

        player_vel_x = 0


        if keys[pygame.K_LEFT]:
            player_vel_x = -player_speed


        if keys[pygame.K_RIGHT]:
            player_vel_x = player_speed


        if keys[pygame.K_UP] and is_grounded:

            player_vel_y = JUMP_STRENGTH

            is_grounded = False


        player_vel_y += GRAVITY


        player_rect.x += player_vel_x


        if player_rect.left < 0:
            player_rect.left = 0


        if player_rect.right > WIDTH:
            player_rect.right = WIDTH


        player_rect.y += player_vel_y

        is_grounded = False


        for platform in platforms:

            if player_rect.colliderect(platform):

                if player_vel_y > 0:

                    player_rect.bottom = platform.top

                    player_vel_y = 0

                    is_grounded = True


                elif player_vel_y < 0:

                    player_rect.top = platform.bottom

                    player_vel_y = 0


        if player_rect.bottom > 550:

            player_rect.bottom = 550

            player_vel_y = 0

            is_grounded = True


        for f in fish[:]:

            if player_rect.colliderect(f):

                fish.remove(f)

                fish_score += 1

                last_fish_time = pygame.time.get_ticks()


        while len(fish) < 10:
            fish.append(make_fish())


        current_time = pygame.time.get_ticks()

        time_passed = (current_time - last_fish_time) / 1000


        if time_passed >= 15:
            game_over = True


        if fish_score >= 100:
            win = True


    screen.fill(BACKGROUND)


    for platform in platforms:
        pygame.draw.rect(screen, BLUE, platform)


    for f in fish:
        screen.blit(fish_image, f)


    screen.blit(cat_image, player_rect)


    score_text = font.render(
        "Fish: " + str(fish_score) + "/100",
        True,
        BLACK
    )

    screen.blit(score_text, (20, 20))


    if not game_over and not win:

        current_time = pygame.time.get_ticks()

        time_passed = (current_time - last_fish_time) / 1000

        time_left = 15 - time_passed


        if time_left < 0:
            time_left = 0


        timer_text = font.render(
            "Time: " + str(round(time_left, 1)),
            True,
            BLACK
        )

        screen.blit(timer_text, (620, 20))


    if game_over:

        lose_text = big_font.render(
            "YOU LOSE",
            True,
            RED
        )

        restart_text = font.render(
            "Press R to restart",
            True,
            BLACK
        )

        screen.blit(
            lose_text,
            (
                WIDTH // 2 - lose_text.get_width() // 2,
                220
            )
        )

        screen.blit(
            restart_text,
            (
                WIDTH // 2 - restart_text.get_width() // 2,
                300
            )
        )


    if win:

        win_text = big_font.render(
            "YOU WIN!",
            True,
            GREEN
        )

        restart_text = font.render(
            "Press R to restart",
            True,
            BLACK
        )

        screen.blit(
            win_text,
            (
                WIDTH // 2 - win_text.get_width() // 2,
                220
            )
        )

        screen.blit(
            restart_text,
            (
                WIDTH // 2 - restart_text.get_width() // 2,
                300
            )
        )


    pygame.display.flip()

    clock.tick(60)


pygame.quit()
sys.exit()
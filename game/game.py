"""
Stickman Defense Game
A shooting defense game where you control a stickman to protect your home!

Controls:
- WASD or Arrow Keys: Move stickman
- Mouse Click or Space: Shoot
- ESC: Pause/Quit
"""

import math
import random
import sys

import pygame

# Initialize Pygame
pygame.init()

# Game Configuration
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
YELLOW = (255, 255, 0)
ORANGE = (255, 140, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
BROWN = (139, 69, 19)
LIGHT_BLUE = (173, 216, 230)

# Game Settings
HOME_X = 50
HOME_WIDTH = 100
HOME_HEIGHT = 150
MAX_MONSTERS_IN_HOME = 5

# Player Settings
PLAYER_SPEED = 30
PLAYER_SIZE = 30
BULLET_SPEED = 10
BULLET_SIZE = 5
SHOOT_COOLDOWN = 15

# Monster Settings
MONSTER_SPEED_MIN = 1
MONSTER_SPEED_MAX = 3
MONSTER_SIZE = 25
SPAWN_RATE = 60
SPAWN_X = SCREEN_WIDTH - 50


class Stickman:
    """Player stickman class"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.shoot_cooldown = 0
        self.facing_right = True

    def update(self, keys):
        """Update player position based on input"""
        dx = 0
        dy = 0

        # Movement
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed
            self.facing_right = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed
            self.facing_right = True
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.speed

        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707

        self.x += dx
        self.y += dy

        # Keep player on screen
        self.x = max(self.size, min(SCREEN_WIDTH - self.size, self.x))
        self.y = max(self.size, min(SCREEN_HEIGHT - self.size, self.y))

        # Update shoot cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def shoot(self, mouse_pos):
        """Create a bullet towards mouse position"""
        if self.shoot_cooldown > 0:
            return None

        self.shoot_cooldown = SHOOT_COOLDOWN

        # Calculate direction to mouse
        dx = mouse_pos[0] - self.x
        dy = mouse_pos[1] - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > 0:
            dx /= distance
            dy /= distance
            self.facing_right = dx > 0
            return Bullet(self.x, self.y, dx, dy)
        return None

    def draw(self, screen):
        """Draw the stickman"""
        x, y = int(self.x), int(self.y)
        size = self.size

        # Head
        pygame.draw.circle(screen, WHITE, (x, y - size // 2), size // 4)

        # Body
        pygame.draw.line(screen, WHITE, (x, y - size // 4), (x, y + size // 4), 3)

        # Arms
        arm_len = size // 3
        if self.facing_right:
            pygame.draw.line(
                screen, WHITE, (x, y - size // 8), (x + arm_len, y - size // 3), 2
            )
            pygame.draw.line(
                screen, WHITE, (x, y), (x - arm_len // 2, y + size // 4), 2
            )
        else:
            pygame.draw.line(
                screen, WHITE, (x, y - size // 8), (x - arm_len, y - size // 3), 2
            )
            pygame.draw.line(
                screen, WHITE, (x, y), (x + arm_len // 2, y + size // 4), 2
            )

        # Legs
        leg_len = size // 3
        pygame.draw.line(
            screen, WHITE, (x, y + size // 4), (x - leg_len // 2, y + size // 2), 2
        )
        pygame.draw.line(
            screen, WHITE, (x, y + size // 4), (x + leg_len // 2, y + size // 2), 2
        )


class Bullet:
    """Bullet class"""

    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx * BULLET_SPEED
        self.dy = dy * BULLET_SPEED
        self.size = BULLET_SIZE
        self.active = True

    def update(self):
        """Update bullet position"""
        self.x += self.dx
        self.y += self.dy
        if self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT:
            self.active = False

    def draw(self, screen):
        """Draw the bullet"""
        if self.active:
            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.size)
            pygame.draw.circle(
                screen, ORANGE, (int(self.x), int(self.y)), self.size // 2
            )


class Monster:
    """Monster class"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = MONSTER_SIZE
        self.speed = random.uniform(MONSTER_SPEED_MIN, MONSTER_SPEED_MAX)
        self.reached_home = False
        self.color = random.choice([RED, ORANGE, (255, 0, 255), (255, 100, 100)])

    def update(self):
        """Update monster position"""
        self.x -= self.speed
        if self.x <= HOME_X + HOME_WIDTH:
            self.reached_home = True

    def draw(self, screen):
        """Draw the monster"""
        x, y = int(self.x), int(self.y)
        size = self.size

        # Body
        pygame.draw.circle(screen, self.color, (x, y), size)

        # Eyes
        eye_size = 3
        eye_x1, eye_x2 = x - size // 3, x + size // 3
        eye_y = y - size // 4
        pygame.draw.circle(screen, WHITE, (eye_x1, eye_y), eye_size)
        pygame.draw.circle(screen, WHITE, (eye_x2, eye_y), eye_size)
        pygame.draw.circle(screen, BLACK, (eye_x1, eye_y), eye_size // 2)
        pygame.draw.circle(screen, BLACK, (eye_x2, eye_y), eye_size // 2)

        # Mouth
        pygame.draw.arc(
            screen, BLACK, (x - size // 2, y, size, size // 2), 0, math.pi, 2
        )

        # Arms
        pygame.draw.line(
            screen, self.color, (x, y + size // 2), (x - size // 2, y + size), 2
        )
        pygame.draw.line(
            screen, self.color, (x, y + size // 2), (x + size // 2, y + size), 2
        )


class Home:
    """Home class"""

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        """Draw the home"""
        # House base
        pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(
            screen, DARK_GRAY, (self.x, self.y, self.width, self.height), 3
        )

        # Roof
        roof_points = [
            (self.x - 10, self.y),
            (self.x + self.width // 2, self.y - 30),
            (self.x + self.width + 10, self.y),
        ]
        pygame.draw.polygon(screen, RED, roof_points)
        pygame.draw.polygon(screen, DARK_GRAY, roof_points, 3)

        # Door
        door_w, door_h = 30, 50
        door_x = self.x + self.width // 2 - door_w // 2
        door_y = self.y + self.height - door_h
        pygame.draw.rect(screen, DARK_GRAY, (door_x, door_y, door_w, door_h))

        # Window
        win_size = 25
        win_x = self.x + self.width // 4
        win_y = self.y + self.height // 3
        pygame.draw.rect(screen, LIGHT_BLUE, (win_x, win_y, win_size, win_size))
        pygame.draw.rect(screen, DARK_GRAY, (win_x, win_y, win_size, win_size), 2)
        pygame.draw.line(
            screen,
            DARK_GRAY,
            (win_x + win_size // 2, win_y),
            (win_x + win_size // 2, win_y + win_size),
            2,
        )
        pygame.draw.line(
            screen,
            DARK_GRAY,
            (win_x, win_y + win_size // 2),
            (win_x + win_size, win_y + win_size // 2),
            2,
        )


class Game:
    """Main game class"""

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Stickman Defense")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)

        self.player = Stickman(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.bullets = []
        self.monsters = []
        self.home = Home(
            HOME_X, SCREEN_HEIGHT - HOME_HEIGHT - 20, HOME_WIDTH, HOME_HEIGHT
        )

        self.running = True
        self.game_over = False
        self.paused = False
        self.score = 0
        self.spawn_timer = 0
        self.monsters_in_home = 0

    def spawn_monster(self):
        """Spawn a new monster"""
        y = random.randint(50, SCREEN_HEIGHT - 50)
        self.monsters.append(Monster(SPAWN_X, y))

    def update(self, keys, mouse_pos, mouse_clicked):
        """Update game state"""
        if self.game_over or self.paused:
            return

        # Update player
        self.player.update(keys)

        # Handle shooting
        if mouse_clicked or keys[pygame.K_SPACE]:
            bullet = self.player.shoot(mouse_pos)
            if bullet:
                self.bullets.append(bullet)

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.active:
                self.bullets.remove(bullet)

        # Spawn monsters
        self.spawn_timer += 1
        if self.spawn_timer >= SPAWN_RATE:
            self.spawn_monster()
            self.spawn_timer = 0

        # Update monsters and check collisions
        for monster in self.monsters[:]:
            monster.update()

            # Check if monster reached home
            if monster.reached_home and monster.x <= HOME_X:
                self.monsters.remove(monster)
                self.monsters_in_home += 1
                if self.monsters_in_home >= MAX_MONSTERS_IN_HOME:
                    self.game_over = True

            # Check bullet collisions
            for bullet in self.bullets[:]:
                if bullet.active:
                    dx = bullet.x - monster.x
                    dy = bullet.y - monster.y
                    distance = math.sqrt(dx * dx + dy * dy)
                    if distance < bullet.size + monster.size:
                        self.bullets.remove(bullet)
                        self.monsters.remove(monster)
                        self.score += 10
                        break

        # Remove monsters off screen
        for monster in self.monsters[:]:
            if monster.x < -monster.size:
                self.monsters.remove(monster)

    def draw(self):
        """Draw everything"""
        # Background
        self.screen.fill((20, 30, 40))
        pygame.draw.rect(
            self.screen, DARK_GRAY, (0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20)
        )

        # Draw game objects
        self.home.draw(self.screen)
        for monster in self.monsters:
            monster.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        self.player.draw(self.screen)

        # Draw UI
        self.draw_ui()

        # Draw overlay
        if self.game_over:
            self.draw_game_over()
        elif self.paused:
            self.draw_pause()

        pygame.display.flip()

    def draw_ui(self):
        """Draw user interface"""
        self.screen.blit(
            self.font_small.render(f"Score: {self.score}", True, WHITE), (10, 10)
        )
        self.screen.blit(
            self.font_small.render(
                f"Monsters in Home: {self.monsters_in_home}/{MAX_MONSTERS_IN_HOME}",
                True,
                RED,
            ),
            (10, 50),
        )
        self.screen.blit(
            self.font_small.render(f"Monsters: {len(self.monsters)}", True, WHITE),
            (10, 90),
        )

        if not self.game_over and not self.paused:
            self.screen.blit(
                self.font_small.render(
                    "WASD: Move | Mouse/Space: Shoot | ESC: Pause", True, GRAY
                ),
                (SCREEN_WIDTH - 450, 10),
            )

    def draw_game_over(self):
        """Draw game over screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        text1 = self.font_large.render("GAME OVER", True, RED)
        self.screen.blit(
            text1, text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        )

        text2 = self.font_medium.render(f"Final Score: {self.score}", True, WHITE)
        self.screen.blit(
            text2, text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        )

        text3 = self.font_small.render("Press R to Restart or ESC to Quit", True, WHITE)
        self.screen.blit(
            text3, text3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        )

    def draw_pause(self):
        """Draw pause screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        text1 = self.font_large.render("PAUSED", True, YELLOW)
        self.screen.blit(
            text1, text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        )

        text2 = self.font_small.render("Press ESC to Resume", True, WHITE)
        self.screen.blit(
            text2, text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        )

    def restart(self):
        """Restart the game"""
        self.player = Stickman(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.bullets = []
        self.monsters = []
        self.game_over = False
        self.paused = False
        self.score = 0
        self.spawn_timer = 0
        self.monsters_in_home = 0

    def run(self):
        """Main game loop"""
        mouse_clicked = False

        while self.running:
            mouse_clicked = False

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_clicked = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.game_over:
                            self.running = False
                        else:
                            self.paused = not self.paused
                    elif event.key == pygame.K_r and self.game_over:
                        self.restart()

            # Update and draw
            if not self.paused:
                self.update(
                    pygame.key.get_pressed(), pygame.mouse.get_pos(), mouse_clicked
                )
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback

        traceback.print_exc()
        pygame.quit()
        sys.exit()

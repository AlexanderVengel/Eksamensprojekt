#skal kunne bevæge sig i forhold til spilleren, eventuelt holde en fast afstand
#skal kunne skyde mod spilleren
#skal have health og damage
#Eventuelt have en cirkel rundt om spileren hvor fjenderne kan bevæge sig i en cirkel på denne cirkel om spilleren

# - Kan gøre dette ved at tage player.x og player.y og derfra tegne en større cirkel om spilleren.
# - På denne store cirkel om spilleren kan man så vælge et punkt
# - Man kan så på dette punkt tegne endnu en cirkel med mindre radius som enemy kan bevæge sig på.
# - På denne måde kan man nok ikke undgå "obstacles" som barrels og lignedne men man har stadig et meget arcade-agtigt spil

import pygame


class enemy:
    def __init__(self, x, y, size=30, speed=2, max_health=40, damage=10):
        self.size = size
        self.speed = speed
        self.position = pygame.Vector2(x, y)

        self.max_health = max_health
        self.health = max_health
        self.damage = damage
        self.alive = True

        self.color = (200, 50, 50)

        # afstand fjenden helst vil have til spilleren
        self.preferred_distance = 220
        self.too_close_distance = 150
        self.too_far_distance = 280

        # hvor meget den cirkler rundt om spilleren
        self.circle_strength = 1.2

        self.hitbox = pygame.Rect(
            self.position.x,
            self.position.y,
            self.size,
            self.size
        )

        # skydning
        self.shoot_cooldown = 90   # frames
        self.shoot_timer = 0

        self.font = pygame.font.SysFont(None, 22)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def update(self, player, barriers, enemy_arrows, screen_width, screen_height):
        if not self.alive:
            return

        player_center = pygame.Vector2(
            player.position.x + player.size / 2,
            player.position.y + player.size / 2
        )

        enemy_center = pygame.Vector2(
            self.position.x + self.size / 2,
            self.position.y + self.size / 2
        )

        to_player = player_center - enemy_center
        distance = to_player.length()

        movement = pygame.Vector2(0, 0)

        if distance > 0:
            direction_to_player = to_player.normalize()

            # tangent-vektor giver cirkelbevægelse rundt om spilleren
            tangent = pygame.Vector2(-direction_to_player.y, direction_to_player.x)

            # hvis fjenden er for langt væk, går den nærmere
            if distance > self.too_far_distance:
                movement += direction_to_player

            # hvis fjenden er for tæt på, går den væk
            elif distance < self.too_close_distance:
                movement -= direction_to_player

            # hvis den er i passende område, cirkler den mere
            else:
                movement += tangent * self.circle_strength

            # bland lidt cirkling ind næsten hele tiden
            movement += tangent * 0.35

        # normaliser bevægelse
        if movement.length() > 0:
            movement = movement.normalize() * self.speed

        old_position = self.position.copy()
        self.position += movement
        self.hitbox.topleft = (self.position.x, self.position.y)

        # collision med barriers
        for barrier in barriers:
            if self.hitbox.colliderect(barrier.hitbox):
                self.position = old_position
                self.hitbox.topleft = (self.position.x, self.position.y)
                break

        # hold fjenden inde på skærmen
        self.position.x = max(0, min(screen_width - self.size, self.position.x))
        self.position.y = max(0, min(screen_height - self.size, self.position.y))
        self.hitbox.topleft = (self.position.x, self.position.y)

        # skyd mod spilleren
        if self.shoot_timer > 0:
            self.shoot_timer -= 1
        else:
            self.shoot(player, enemy_arrows)
            self.shoot_timer = self.shoot_cooldown

    def shoot(self, player, enemy_arrows):
        player_center = pygame.Vector2(
            player.position.x + player.size / 2,
            player.position.y + player.size / 2
        )

        enemy_center = pygame.Vector2(
            self.position.x + self.size / 2,
            self.position.y + self.size / 2
        )

        arrow = EnemyArrow(
            x=enemy_center.x,
            y=enemy_center.y,
            speed=6,
            size=6,
            target_pos=player_center,
            damage=self.damage
        )

        enemy_arrows.append(arrow)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.hitbox)

        # health bar
        health_ratio = self.health / self.max_health
        bar_width = self.size
        bar_height = 5
        bar_x = self.hitbox.left
        bar_y = self.hitbox.top - 10

        pygame.draw.rect(screen, (200, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 200, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))

        text_surface = self.font.render(str(int(self.health)), True, (0, 0, 0))
        screen.blit(text_surface, (self.hitbox.left, self.hitbox.top - 28))


class EnemyArrow:
    def __init__(self, x, y, speed, size, target_pos, damage=10):
        self.size = size
        self.speed = speed
        self.damage = damage
        self.position = pygame.Vector2(x, y)

        self.hitbox = pygame.Rect(
            self.position.x - self.size,
            self.position.y - self.size,
            self.size * 2,
            self.size * 2
        )

        direction = pygame.Vector2(target_pos) - self.position
        if direction.length() != 0:
            self.direction = direction.normalize()
        else:
            self.direction = pygame.Vector2(0, 0)

        self.alive = True

    def update(self, screen_width, screen_height):
        self.position += self.direction * self.speed
        self.hitbox.center = (self.position.x, self.position.y)

        if (
            self.position.x < 0 or self.position.x > screen_width or
            self.position.y < 0 or self.position.y > screen_height
        ):
            self.alive = False

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (255, 120, 0),
            (int(self.position.x), int(self.position.y)),
            self.size
        )
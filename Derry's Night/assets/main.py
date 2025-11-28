import pygame
import math
import sys

# ===== 1. CONFIGURAÇÕES =====
class Settings:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    HALF_HEIGHT = SCREEN_HEIGHT // 2
    FPS = 60
    
    # Raycasting
    FOV = math.pi / 3
    HALF_FOV = FOV / 2
    NUM_RAYS = SCREEN_WIDTH // 2 
    DELTA_ANGLE = FOV / NUM_RAYS
    MAX_DEPTH = 60
    SCALE = SCREEN_WIDTH // NUM_RAYS 
    
    TEXTURE_SIZE = 64

# ===== 2. MAPA COMPLEXO (60x60) =====
MAPA = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,1,2,2,2,2,2,1,1,1,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1],
    [1,0,0,1,2,1,1,1,2,1,1,2,2,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,2,2,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1],
    [1,0,0,2,2,1,1,1,2,2,2,2,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1],
    [1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,0,0,0,1,1,1,2,2,2,2,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1],
    [1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,0,0,0,0,0,1,2,2,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,2,2,2,2,1,1,2,1,1,1,1,1,1,1],
    [1,1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,2,1,0,0,1,0,0,1,2,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,1,1,2,1,1,2,2,2,2,2,2,2,1],
    [1,1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,2,2,2,2,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,2,1],
    [1,1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1,1,1,2,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,1,1,2,1],
    [1,1,2,1,1,1,1,2,2,2,2,2,1,2,1,1,1,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,1,1,1,1,1,2,1,1,2,1],
    [1,1,2,1,1,1,2,2,1,1,1,2,1,2,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,3,3,3,2,2,3,3,3,1,1,2,1,1,2,1],
    [1,1,2,1,1,2,2,1,1,1,1,2,2,2,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,3,3,2,2,2,2,2,2,3,3,1,2,1,1,2,1],
    [1,1,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,3,3,2,2,3,3,3,3,2,2,3,3,1,2,1,1,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,3,2,2,3,1,1,1,1,3,2,2,3,1,2,2,2,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,3,2,2,3,1,1,1,1,1,1,3,2,2,3,1,1,1,1,1],
    [1,2,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,3,3,2,2,3,1,1,1,1,1,1,1,1,3,2,3,3,1,1,1,1],
    [1,2,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,3,2,2,3,3,1,1,1,2,2,2,1,1,3,2,2,3,1,1,1,1],
    [1,2,1,1,1,1,2,2,2,2,2,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,3,2,2,3,1,1,1,2,2,1,2,2,1,1,3,2,3,1,1,1,1],
    [1,2,1,1,1,2,2,1,1,1,2,2,1,2,1,1,1,1,1,2,2,2,2,2,2,2,1,1,2,2,2,2,2,1,1,1,1,1,1,3,2,2,3,1,1,2,2,1,1,1,2,2,1,3,2,3,1,1,1,1],
    [1,2,1,1,2,2,1,1,1,1,1,2,2,2,1,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,3,3,2,3,1,1,2,1,1,1,1,1,2,1,3,2,3,1,1,1,1],
    [1,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,1,3,2,3,1,2,2,1,1,1,1,1,2,1,3,2,3,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,2,2,2,2,2,2,2,2,2,1,1,1,3,2,3,1,2,1,1,1,1,1,1,2,1,3,2,3,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,1,2,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,1,3,2,3,1,2,1,1,1,1,1,1,2,1,3,2,3,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,2,1,2,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,1,2,1,1,3,3,2,3,3,2,1,1,1,1,1,1,2,1,3,2,3,1,1,1,1],
    [1,2,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,2,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,2,1,1,3,2,2,2,3,2,2,2,2,2,2,2,2,1,3,2,3,1,1,1,1],
    [1,2,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,2,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,2,1,1,3,2,2,2,3,3,3,3,3,3,3,3,3,1,3,2,3,1,1,1,1],
    [1,2,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2,1,1,1,1,1,2,2,2,2,2,2,2,1,1,2,1,2,1,1,3,3,2,2,2,2,2,2,2,2,2,2,3,3,3,2,3,1,1,1,1],
    [1,2,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1,2,1,1,2,2,2,1,1,1,3,3,3,3,3,3,3,3,3,3,2,3,2,2,2,3,1,1,1,1],
    [1,2,2,2,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,2,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,2,3,2,1,1,1,1,1,1,1],
    [1,1,1,2,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,2,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,2,3,2,1,1,1,1,1,1,1],
    [1,1,1,2,1,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,1,2,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,2,3,2,1,1,1,1,1,1,1],
    [1,1,1,2,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,1,2,1,1,2,2,2,1,1,1,1,1,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,3,2,3,2,1,1,1,1,1,1,1],
    [1,1,1,2,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,2,2,2,2,2,3,2,3,2,3,3,3,3,3,3,1],
    [1,1,1,2,2,2,1,1,2,2,2,2,2,2,2,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,2,1,1,1,1,3,2,3,2,3,2,2,2,2,3,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,2,1,1,1,1,1,1,2,1,1,1,1,3,2,3,3,3,2,3,3,2,3,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,1,1,1,1,3,2,2,2,2,2,3,3,2,3,1],
    [1,2,1,1,1,1,1,1,1,1,1,1,2,1,2,1,1,1,2,2,2,2,2,2,2,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,2,3,1],
    [1,2,1,1,1,1,1,1,1,1,1,1,2,1,2,1,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1,1,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,3,1],
    [1,2,2,2,2,2,2,1,1,2,2,2,2,1,2,1,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,3,1],
    [1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1,1,1,2,2,2,2,1,1,2,2,2,2,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,1],
    [1,0,0,0,0,1,2,1,1,2,1,1,1,1,2,1,1,1,1,1,1,2,1,1,1,1,1,2,1,2,1,1,2,2,2,2,2,1,2,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,1,2,2,2,2,1,1,1,1,2,1,1,1,1,1,1,2,1,1,1,1,1,2,1,2,1,1,1,1,1,1,2,1,2,1,1,1,1,1,2,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,1,1,1,1,1,2,2,2,1,1,1,1,1,1,2,1,2,1,1,1,1,1,2,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,2,2,2,2,2,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,2,1,2,1,1,1,1,1,1,1,3,3,3,3,3,3,3,1],
    [1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,1,1,2,1,2,1,1,1,1,1,1,1,3,2,2,2,2,2,3,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,1,1,2,1,2,2,2,2,2,2,2,2,3,2,3,3,3,2,3,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,3,2,3,1,3,2,3,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,1,1,1,1,1,1,1,1,1,3,2,3,1,3,2,3,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,1,3,3,3,1],
]

# ===== 3. CLASSE DO JOGADOR =====
class Player:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 4.0
        self.rot_speed = 2.5
        self.collision_margin = 0.2

    def movement(self, dt):
        keys = pygame.key.get_pressed()
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx = 0; dy = 0
        speed = self.speed * dt
        rot_speed = self.rot_speed * dt

        if keys[pygame.K_LEFT]: self.angle -= rot_speed
        if keys[pygame.K_RIGHT]: self.angle += rot_speed
        if keys[pygame.K_w] or keys[pygame.K_UP]: dx += cos_a * speed; dy += sin_a * speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: dx -= cos_a * speed; dy -= sin_a * speed
        if keys[pygame.K_a]: dx += sin_a * speed; dy -= cos_a * speed
        if keys[pygame.K_d]: dx -= sin_a * speed; dy += cos_a * speed
        self.check_collision(dx, dy)

    def check_collision(self, dx, dy):
        next_x = self.x + dx
        scale_x = self.collision_margin if dx > 0 else -self.collision_margin
        if MAPA[int(self.y)][int(next_x + scale_x)] in (0, 2): self.x = next_x
        next_y = self.y + dy
        scale_y = self.collision_margin if dy > 0 else -self.collision_margin
        if MAPA[int(next_y + scale_y)][int(self.x)] in (0, 2): self.y = next_y
    @property
    def pos(self): return (self.x, self.y)
    @property
    def map_pos(self): return (int(self.x), int(self.y))

# ===== 4. OBJETOS (SPRITES DINÂMICOS) =====
class SpriteObject:
    def __init__(self, x, y, texture, visible=True):
        self.x = x
        self.y = y
        self.texture = texture
        self.visible = visible
        self.is_eyes = False 

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprites = []
        
        self.tex_stone = self.generate_stone_tex()
        self.tex_eyes = self.generate_eyes_tex()

        self.find_dead_ends_and_populate()
        
        # --- PEDRA DE TESTE (GARANTIDA) ---
        # Coloca a 1 bloco de distância do jogador
        test_x = 4.5 
        test_y = 2.5
        stone_test = SpriteObject(test_x, test_y, self.tex_stone, visible=True)
        eyes_test = SpriteObject(test_x, test_y, self.tex_eyes, visible=False)
        eyes_test.is_eyes = True
        eyes_test.linked_stone = stone_test
        self.sprites.append(stone_test)
        self.sprites.append(eyes_test)

    def find_dead_ends_and_populate(self):
        rows = len(MAPA)
        cols = len(MAPA[0])
        # Varre o mapa com segurança
        for y in range(rows):
            for x in range(cols):
                if MAPA[y][x] in (0, 2): # Se é chão
                    walls = 0
                    # Checa vizinhos com verificação de limites (CORREÇÃO DE CRASH)
                    if y > 0 and MAPA[y-1][x] in (1, 3): walls += 1
                    if y < rows - 1 and MAPA[y+1][x] in (1, 3): walls += 1
                    if x > 0 and MAPA[y][x-1] in (1, 3): walls += 1
                    if x < cols - 1 and MAPA[y][x+1] in (1, 3): walls += 1
                    
                    if walls >= 3:
                        # Evita spawn inicial
                        if x < 6 and y < 6: continue
                        
                        stone = SpriteObject(x + 0.5, y + 0.5, self.tex_stone, visible=True)
                        eyes = SpriteObject(x + 0.5, y + 0.5, self.tex_eyes, visible=False)
                        eyes.is_eyes = True
                        eyes.linked_stone = stone 
                        self.sprites.append(stone)
                        self.sprites.append(eyes)

    def generate_stone_tex(self):
        s = pygame.Surface((64, 64), pygame.SRCALPHA)
        # Pedra BRANCA/CINZA CLARO para testar visibilidade
        pygame.draw.circle(s, (200, 200, 200), (32, 45), 15) 
        pygame.draw.circle(s, (50, 50, 50), (32, 45), 15, 2) # Borda
        return s

    def generate_eyes_tex(self):
        s = pygame.Surface((64, 64), pygame.SRCALPHA)
        # Olhos Amarelos e Grandes
        pygame.draw.circle(s, (255, 255, 0), (20, 25), 6) 
        pygame.draw.circle(s, (255, 255, 0), (44, 25), 6)
        # Pupila vermelha para assustar
        pygame.draw.circle(s, (255, 0, 0), (20, 25), 2)
        pygame.draw.circle(s, (255, 0, 0), (44, 25), 2)
        return s

    def update(self):
        player_x = self.game.player.x
        player_y = self.game.player.y
        keys = pygame.key.get_pressed()
        
        # Teleporte Q
        front_x = player_x + math.cos(self.game.player.angle) * 1.0
        front_y = player_y + math.sin(self.game.player.angle) * 1.0
        if keys[pygame.K_q]:
            if 0 <= front_y < len(MAPA) and 0 <= front_x < len(MAPA[0]):
                if MAPA[int(front_y)][int(front_x)] == 3:
                    self.game.player.x = 30.5; self.game.player.y = 30.5
                    print("TELETRANSPORTADO...")

        # Pedra E
        if keys[pygame.K_e]:
            for sprite in self.sprites:
                if not sprite.is_eyes and sprite.visible:
                    dist = math.hypot(player_x - sprite.x, player_y - sprite.y)
                    if dist < 1.5:
                        sprite.visible = False 
                        for s in self.sprites:
                            if s.is_eyes and getattr(s, 'linked_stone', None) == sprite:
                                s.visible = True
                        print("PEGOU A PEDRA!")

# ===== 5. RAYCASTER =====
class Raycaster:
    def __init__(self, game):
        self.game = game
        self.textures = self.load_textures()
        self.z_buffer = [0] * Settings.NUM_RAYS

    def load_textures(self):
        def get_tex(path, color):
            try:
                tex = pygame.image.load(path).convert()
                return pygame.transform.scale(tex, (Settings.TEXTURE_SIZE, Settings.TEXTURE_SIZE))
            except:
                surf = pygame.Surface((Settings.TEXTURE_SIZE, Settings.TEXTURE_SIZE))
                surf.fill(color); pygame.draw.rect(surf,(0,0,0),(0,0,Settings.TEXTURE_SIZE,Settings.TEXTURE_SIZE),1)
                return surf
        return { 1: get_tex("textures/wall_concrete.png", (100, 100, 100)),
                 2: get_tex("textures/water.png", (50, 50, 200)),
                 3: get_tex("textures/room_stained.png", (150, 50, 50)) }

    def cast_rays(self):
        ox, oy = self.game.player.pos
        map_x, map_y = self.game.player.map_pos
        ray_angle = self.game.player.angle - Settings.HALF_FOV + 0.0001

        for ray in range(0, Settings.NUM_RAYS):
            sin_a, cos_a = math.sin(ray_angle), math.cos(ray_angle)
            x_map, y_map = map_x, map_y
            delta_dist_x = abs(1 / cos_a) if cos_a != 0 else 1e30
            delta_dist_y = abs(1 / sin_a) if sin_a != 0 else 1e30
            if cos_a < 0: step_x = -1; side_dist_x = (ox - x_map) * delta_dist_x
            else: step_x = 1; side_dist_x = (x_map + 1.0 - ox) * delta_dist_x
            if sin_a < 0: step_y = -1; side_dist_y = (oy - y_map) * delta_dist_y
            else: step_y = 1; side_dist_y = (y_map + 1.0 - oy) * delta_dist_y
            texture_vert = 0; hit_side = 0
            
            for _ in range(Settings.MAX_DEPTH):
                if side_dist_x < side_dist_y: side_dist_x += delta_dist_x; x_map += step_x; hit_side = 0
                else: side_dist_y += delta_dist_y; y_map += step_y; hit_side = 1
                if not (0 <= y_map < len(MAPA) and 0 <= x_map < len(MAPA[0])): break
                tile = MAPA[y_map][x_map]
                if tile > 0 and tile != 2: texture_vert = tile; break
                
            if texture_vert:
                if hit_side == 0: perp_dist = (side_dist_x - delta_dist_x)
                else: perp_dist = (side_dist_y - delta_dist_y)
                perp_dist *= math.cos(self.game.player.angle - ray_angle)
                if perp_dist < 0.001: perp_dist = 0.001
                
                self.z_buffer[ray] = perp_dist 

                proj_height = int(Settings.SCREEN_HEIGHT / perp_dist)
                if hit_side == 0: wall_x = oy + perp_dist * sin_a
                else: wall_x = ox + perp_dist * cos_a
                wall_x -= math.floor(wall_x); tex_x = int(wall_x * Settings.TEXTURE_SIZE)
                if (hit_side == 0 and cos_a > 0) or (hit_side == 1 and sin_a < 0): tex_x = Settings.TEXTURE_SIZE - tex_x - 1
                tex = self.textures.get(texture_vert)
                col = tex.subsurface((tex_x, 0, 1, Settings.TEXTURE_SIZE))
                col_scaled = pygame.transform.scale(col, (Settings.SCALE, proj_height))
                shade = 255 / (1 + perp_dist ** 2 * 0.015); shade = max(5, min(255, shade))
                if hit_side == 1: shade *= 0.7
                col_scaled.fill((shade, shade, shade), special_flags=pygame.BLEND_MULT)
                render_pos = (Settings.HALF_HEIGHT - proj_height // 2)
                self.game.screen.blit(col_scaled, (ray * Settings.SCALE, render_pos))
            ray_angle += Settings.DELTA_ANGLE

    def cast_sprites(self):
        sprites = [s for s in self.game.object_handler.sprites if s.visible]
        sprites.sort(key=lambda s: math.hypot(self.game.player.x - s.x, self.game.player.y - s.y), reverse=True)

        for sprite in sprites:
            dx = sprite.x - self.game.player.x
            dy = sprite.y - self.game.player.y
            dist = math.hypot(dx, dy)
            
            sprite_angle = math.atan2(dy, dx)
            delta = sprite_angle - self.game.player.angle
            if (dx > 0 and self.game.player.angle > math.pi) or (dx < 0 and dy < 0): delta += math.tau
            delta_rays = delta / Settings.DELTA_ANGLE
            screen_x = (Settings.NUM_RAYS / 2 + delta_rays) * Settings.SCALE
            
            dist *= math.cos(Settings.HALF_FOV - delta_rays * Settings.DELTA_ANGLE)
            if dist < 0.1: continue

            proj_height = int(Settings.SCREEN_HEIGHT / dist)
            sprite_w = int(proj_height * (sprite.texture.get_width() / sprite.texture.get_height()))
            sprite_scaled = pygame.transform.scale(sprite.texture, (sprite_w, proj_height))
            
            # Ajuste de altura para ficarem no chão ou parede
            v_offset = int(proj_height * 0.3) if not sprite.is_eyes else -int(proj_height * 0.2)
            
            sprite_y = Settings.HALF_HEIGHT - proj_height // 2 + v_offset
            start_x = int(screen_x - sprite_w // 2)
            
            for x in range(start_x, start_x + sprite_w):
                if 0 <= x < Settings.SCREEN_WIDTH:
                    ray_idx = int(x // Settings.SCALE)
                    if ray_idx < len(self.z_buffer) and self.z_buffer[ray_idx] > dist:
                        tex_x = int((x - start_x) * (sprite_scaled.get_width() / sprite_w))
                        col = sprite_scaled.subsurface((tex_x, 0, 1, proj_height))
                        self.game.screen.blit(col, (x, sprite_y))

# ===== 6. CLASSE GAME =====
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Derry Sewers - Stone Fixed")
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.new_game()
        
    def new_game(self):
        self.player = Player(2.5, 2.5, 0)
        self.object_handler = ObjectHandler(self)
        self.raycaster = Raycaster(self)

    def draw_gradient_background(self):
        for y in range(Settings.HALF_HEIGHT):
            intensity = int(40 * (1 - y / Settings.HALF_HEIGHT))
            pygame.draw.line(self.screen, (intensity, intensity, intensity), (0, y), (Settings.SCREEN_WIDTH, y))
        for y in range(Settings.HALF_HEIGHT, Settings.SCREEN_HEIGHT):
            prog = (y - Settings.HALF_HEIGHT) / Settings.HALF_HEIGHT
            r = int(30 * prog); g = int(40 * prog); b = int(20 * prog)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (Settings.SCREEN_WIDTH, y))

    def update(self):
        dt_seconds = self.delta_time / 1000.0
        self.player.movement(dt_seconds)
        self.object_handler.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(Settings.FPS)

    def draw(self):
        self.draw_gradient_background()
        self.raycaster.cast_rays()
        self.raycaster.cast_sprites()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            self.draw()
            self.update()

if __name__ == "__main__":
    game = Game()
    game.run()
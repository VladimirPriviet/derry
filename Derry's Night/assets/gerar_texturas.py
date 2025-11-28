import pygame
import os
import random

def criar_texturas():
    pygame.init()
    
    # Cria a pasta textures se não existir
    if not os.path.exists("textures"):
        os.makedirs("textures")
        print("Pasta 'textures' criada.")

    size = 64  # Tamanho da textura (padrão retro)

    # --- 1. CONCRETO SUJO (Cinza com ruído e manchas) ---
    surf = pygame.Surface((size, size))
    surf.fill((80, 80, 80)) # Base cinza escuro
    
    # Adiciona ruído (sujeira)
    for _ in range(600):
        x, y = random.randint(0, size-1), random.randint(0, size-1)
        cor = random.randint(40, 100)
        surf.set_at((x, y), (cor, cor, cor))
        
    # Adiciona manchas escuras (limo)
    for _ in range(50):
        x, y = random.randint(0, size-5), random.randint(0, size-5)
        pygame.draw.circle(surf, (40, 50, 40), (x, y), random.randint(2, 6))

    pygame.image.save(surf, "textures/wall_concrete.png")
    print("Salvo: textures/wall_concrete.png")

    # --- 2. TIJOLOS VELHOS (Esgoto clássico) ---
    surf = pygame.Surface((size, size))
    surf.fill((70, 30, 20)) # Vermelho tijolo escuro/podre
    
    # Desenha o rejunte (linhas pretas)
    brick_h = 16
    for row in range(0, size, brick_h):
        pygame.draw.line(surf, (10, 10, 10), (0, row), (size, row), 2)
        # Linhas verticais desencontradas
        offset = 0 if (row // brick_h) % 2 == 0 else (size // 2)
        pygame.draw.line(surf, (10, 10, 10), (offset, row), (offset, row + brick_h), 2)
        pygame.draw.line(surf, (10, 10, 10), (offset + size//2, row), (offset + size//2, row + brick_h), 2)

    # Adiciona "musgo" verde escuro por cima
    for _ in range(400):
        x, y = random.randint(0, size-1), random.randint(0, size-1)
        surf.set_at((x, y), (20, 40, 20))

    pygame.image.save(surf, "textures/room_stained.png")
    print("Salvo: textures/room_stained.png")

    # --- 3. ÁGUA ESCURA (Para efeitos) ---
    surf = pygame.Surface((size, size))
    surf.fill((20, 30, 20)) # Verde pântano bem escuro
    
    # Ondas/Reflexos sutis
    for _ in range(200):
        x, y = random.randint(0, size-1), random.randint(0, size-1)
        surf.set_at((x, y), (30, 50, 30)) # Um pouco mais claro

    pygame.image.save(surf, "textures/water.png")
    print("Salvo: textures/water.png")
    
    print("\nSUCESSO! Agora rode o seu arquivo 'main.py'.")

if __name__ == "__main__":
    criar_texturas()
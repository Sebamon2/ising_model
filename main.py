import pygame
import numpy as np

N = 100
CELL_SIZE = 6
J = 1.0  # Ferromagnético >0 , antiferromagnético <0

B = 0.0  
T = 2.27 

# Estado inicial
grid = np.random.choice([1, -1], size=(N, N))

pygame.init() 
WIDTH, HEIGHT = N * CELL_SIZE, N * CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"Ising | T = {T:.2f} | B = {B:.2f}")

COLOR_UP = (255, 255, 255)  # Blanco (+1)
COLOR_DOWN = (0, 0, 0)      # Negro (-1)


def calculate_delta_e(i, j):
    S_i = grid[i, j]
    S_neighbors = (
        grid[(i - 1) % N, j] +
        grid[(i + 1) % N, j] +
        grid[i, (j - 1) % N] +
        grid[i, (j + 1) % N]
    )
    delta_E = 2 * S_i * (J * S_neighbors + B)
    return delta_E

def metropolis_step():
    global grid
    i, j = np.random.randint(0, N, 2)
    delta_E = calculate_delta_e(i, j)
    
    if delta_E < 0:
        grid[i, j] *= -1
    else:
        if T > 0:
            prob = np.exp(-delta_E / T)
            if np.random.rand() < prob:
                grid[i, j] *= -1

def draw_grid():
    screen.fill((100, 100, 100)) 
    
    for i in range(N):
        for j in range(N):
            rect = (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[i, j] == 1:
                pygame.draw.rect(screen, COLOR_UP, rect)
            else:
                pygame.draw.rect(screen, COLOR_DOWN, rect)
    
    pygame.display.set_caption(f"Ising | T = {T:.2f} | B = {B:.2f} | J = {J:.2f}")


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: running = False
            if event.key == pygame.K_SPACE: grid = np.random.choice([1, -1], size=(N, N))
    
    keys = pygame.key.get_pressed()
    
    # Control de Temperatura (Arriba/Abajo)
    if keys[pygame.K_UP]: T += 0.05
    if keys[pygame.K_DOWN]: T = max(0.01, T - 0.05)
        
    # Control de Campo Magnético (Derecha/Izquierda)
    if keys[pygame.K_RIGHT]: B += 0.05
    if keys[pygame.K_LEFT]: B -= 0.05

    for _ in range(N * N):
        metropolis_step()

    draw_grid()
    pygame.display.flip()

pygame.quit()
import pygame
import random

from ten_drops import WINDOW
from ten_drops.drop import Drop
from ten_drops.droplet import Droplet, Direction

grid: list[list[None | Drop]] = [[None for _ in range(10)] for _ in range(10)]
for row in range(10):
    for col in range(10):
        if random.random() < 0.3:
            grid[row][col] = Drop(row, col)

run = True
all_droplets = []
clock = pygame.time.Clock()

while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col = mouse_x // 40
            row = mouse_y // 40
            if grid[row][col] is not None:
                if grid[row][col].update():
                    for direction in [Direction.Down, Direction.Up, Direction.Left, Direction.Right]:
                        all_droplets.append(Droplet(row, col, direction, 0.1))
                    grid[row][col] = None

    WINDOW.fill((255, 255, 255))

    for row in range(10):
        for col in range(10):
            if grid[row][col] is not None:
                grid[row][col].draw()

    for droplet in all_droplets[:]:
        new_droplet = droplet.move(grid)
        if new_droplet is not None:
            new_droplet.draw()
        else:
            all_droplets.remove(droplet)

    pygame.display.update()

    all_exploded = True
    for row in grid:
        for drop in row:
            if drop is not None:
                all_exploded = False
                break
    if all_exploded:
        print("win!")
        run = False

pygame.quit()

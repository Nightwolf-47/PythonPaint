import pygame
import time

pygame.init()

pygame.display.set_mode((640,480))

pygame.display.set_caption('Test')

programRunning = True
lastFrameTime = 0

def update(dt):
    pass

def keypressed(key):
    pass

def keyreleased(key):
    pass

def mousepressed(x,y):
    pass

def mousereleased(x,y):
    pass

while programRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            programRunning = False
        if event.type == pygame.KEYDOWN:
            keypressed(event.key)
        if event.type == pygame.KEYUP:
            keyreleased(event.key)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousepressed(*pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONUP:
            mousereleased(*pygame.mouse.get_pos())
    currentTime = time.time()
    dt = currentTime - lastFrameTime
    lastFrameTime = currentTime
    update(dt)
    pygame.display.flip()

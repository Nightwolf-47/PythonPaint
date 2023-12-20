import pygame

pygame.init()

from guidefs import *

pygame.display.set_caption('Python Paint')

# test_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(100,100,100,100), text="test", manager=manager)

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

def uievent(event):
    handle_windows(event)
    handle_toolbar(event)

while programRunning:
    dt = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            programRunning = False
        if event.type == pygame.KEYDOWN:
            keypressed(event.key)
        if event.type == pygame.KEYUP:
            keyreleased(event.key)
        if "ui_element" in event.__dict__:
            uievent(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousepressed(*pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONUP:
            mousereleased(*pygame.mouse.get_pos())
        manager.process_events(event)
        
    update(dt)
    manager.update(dt)
    window.blit(background,(0,0))
    manager.draw_ui(window)
    pygame.display.flip()

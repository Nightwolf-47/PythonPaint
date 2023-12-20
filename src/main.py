import pygame

pygame.init()

from guidefs import *

import paint

pygame.display.set_caption('Python Paint')

programRunning = True
lastFrameTime = 0

def update(dt):
    if pygame.mouse.get_pressed()[0] and not manager.hovering_any_ui_element:
        x,y = pygame.mouse.get_pos()
        if x > 150:
            color = colors[0]
            x -= 150
            x = int(x/paint.image_scale)
            y = int(y/paint.image_scale)
            if paint.current_tool == "Pencil":
                color = colors[0]
                paint.draw((x,y),(color.r,color.g,color.b))
            elif paint.current_tool == "Eraser":
                color = colors[1]
                paint.draw((x,y),(color.r,color.g,color.b))

def keypressed(key):
    pass

def keyreleased(key):
    pass

def mousepressed(x,y):
    if paint.current_tool == "Flood Fill" and not manager.hovering_any_ui_element:
        if pygame.mouse.get_pressed()[0]:
            x,y = pygame.mouse.get_pos()
            if x > 150:
                color = colors[0]
                x -= 150
                x = int(x/paint.image_scale)
                y = int(y/paint.image_scale)
                paint.flood_fill((x,y),(color.r,color.g,color.b))    

def mousereleased(x,y):
    paint.last_draw_point = None

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
    if paint.img_surface != None:
        window.blit(pygame.transform.scale(paint.img_surface,tuple(paint.rendered_imgsize)),(150,0))
    manager.draw_ui(window)
    pygame.display.flip()

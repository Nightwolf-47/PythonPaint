import pygame
import pygame_gui
import paint
import os

window = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

manager = pygame_gui.UIManager(pygame.display.get_window_size())

toolpanel = pygame_gui.elements.UIPanel(pygame.Rect(0,0,150,3000),10,manager)

background = pygame.Surface((800,600))

colors = paint.colors

def color_to_hexstring(color):
    return f"#{color.r:02X}{color.g:02X}{color.b:02X}"

toolpanel_elements = {
    'label1': pygame_gui.elements.UILabel(pygame.Rect(10,10,125,20),"Current tool",manager,toolpanel),
    'toolpicker': pygame_gui.elements.UIDropDownMenu(["Pencil","Eraser","Flood Fill"],"Pencil",pygame.Rect(10,30,125,30),manager,toolpanel),
    'colorlabel1': pygame_gui.elements.UILabel(pygame.Rect(10,70,125,20),"Primary color",manager,toolpanel),
    'color1': pygame_gui.elements.UIButton(pygame.Rect(10,90,125,30),color_to_hexstring(colors[0]),manager,toolpanel,"Primary Color"),
    'colorlabel2': pygame_gui.elements.UILabel(pygame.Rect(10,130,125,20),"Secondary color",manager,toolpanel),
    'color2': pygame_gui.elements.UIButton(pygame.Rect(10,150,125,30),color_to_hexstring(colors[1]),manager,toolpanel,"Secondary Color"),
    'label2': pygame_gui.elements.UILabel(pygame.Rect(10,190,125,20),"Brush size",manager,toolpanel),
    'brushsize': pygame_gui.elements.UIDropDownMenu(["1","3","5","11","21"],"1",pygame.Rect(10,210,125,30),manager,toolpanel),
    'new': pygame_gui.elements.UIButton(pygame.Rect(10,280,125,30),"New",manager,toolpanel,"Create new image"),
    'load': pygame_gui.elements.UIButton(pygame.Rect(10,320,125,30),"Load",manager,toolpanel,"Load image from a file"),
    'save': pygame_gui.elements.UIButton(pygame.Rect(10,360,125,30),"Save",manager,toolpanel,"Save image to a file",visible=0),
}

def initialize_program(imgx,imgy):
    global window, background
    if paint.image_scale > 1:
        imgx = int(imgx*paint.image_scale)
        imgy = int(imgy*paint.image_scale)
    winx = max(imgx + 150,640)
    winy = max(imgy, 480)
    window = pygame.display.set_mode((winx,winy))
    manager.set_window_resolution((winx,winy))
    toolpanel.set_dimensions((150,winy))
    background = pygame.Surface((winx,winy))
    toolpanel_elements['save'].visible = True

def load_image(path):
    imgsize = paint.open_image(path)
    if imgsize != None:
        initialize_program(*imgsize)

def handle_toolbar(event):
    if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
        if event.ui_element == toolpanel_elements["toolpicker"]:
            paint.current_tool = event.text
        elif event.ui_element == toolpanel_elements["brushsize"]:
            paint.brush_size = int(event.text)
    if event.type == pygame_gui.UI_BUTTON_PRESSED:
        if event.ui_element == toolpanel_elements['color1']:
            pygame_gui.windows.UIColourPickerDialog(pygame.Rect(0,0,640,480),manager, initial_colour=colors[0], window_title="Choose primary color...", object_id="color1")
        elif event.ui_element == toolpanel_elements['color2']:
            pygame_gui.windows.UIColourPickerDialog(pygame.Rect(0,0,640,480),manager, initial_colour=colors[1], window_title="Choose secondary color...", object_id="color2")
        elif event.ui_element == toolpanel_elements['new']:
            pass
        elif event.ui_element == toolpanel_elements['load']:
            pygame_gui.windows.UIFileDialog(pygame.Rect(0,0,640,480),manager,"Load file...",{'.png','.jpg','.bmp'},os.path.curdir,object_id="loadfile")
        elif event.ui_element == toolpanel_elements['save']:
            pygame_gui.windows.UIFileDialog(pygame.Rect(0,0,640,480),manager,"Save file...",{'.png','.jpg','.bmp'},os.path.curdir,object_id="savefile")
        else:
            return


def handle_windows(event):
    if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
        if event.ui_object_id == "savefile":
            if paint.save_image(event.text):
                pygame_gui.windows.UIMessageWindow(pygame.Rect(0,0,250,160),"File saved successfully!",manager,window_title="Save File Success")
            else:
                pygame_gui.windows.UIMessageWindow(pygame.Rect(0,0,250,160),"File couldn't be saved!",manager,window_title="Save File Failure")
        if event.ui_object_id == "loadfile":
            load_image(event.text)
    if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
        if event.ui_object_id == "color1":
            colors[0] = event.colour
            toolpanel_elements["color1"].set_text(color_to_hexstring(colors[0]))
        if event.ui_object_id == "color2":
            colors[1] = event.colour
            toolpanel_elements["color2"].set_text(color_to_hexstring(colors[1]))

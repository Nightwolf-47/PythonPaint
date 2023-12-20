import pygame
import pygame_gui

window = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()

manager = pygame_gui.UIManager(pygame.display.get_window_size())

toolpanel = pygame_gui.elements.UIPanel(pygame.Rect(0,0,150,3000),10,manager)

background = pygame.Surface((1920,1080))

colors = [pygame.Color(255,255,255), pygame.Color(0,0,0)]

def color_to_hexstring(color):
    return f"#{color.r:02X}{color.g:02X}{color.b:02X}"

toolpanel_elements = {
    'label1': pygame_gui.elements.UILabel(pygame.Rect(10,10,125,20),"Current tool",manager,toolpanel),
    'toolpicker': pygame_gui.elements.UIDropDownMenu(["Pencil","Eraser","Flood Fill"],"Pencil",pygame.Rect(10,30,125,30),manager,toolpanel),
    'colorlabel1': pygame_gui.elements.UILabel(pygame.Rect(10,70,125,20),"Primary color",manager,toolpanel),
    'color1': pygame_gui.elements.UIButton(pygame.Rect(10,90,125,30),color_to_hexstring(colors[0]),manager,toolpanel,"Primary Color"),
    'colorlabel2': pygame_gui.elements.UILabel(pygame.Rect(10,130,125,20),"Secondary color",manager,toolpanel),
    'color2': pygame_gui.elements.UIButton(pygame.Rect(10,150,125,30),color_to_hexstring(colors[1]),manager,toolpanel,"Secondary Color"),
    'new': pygame_gui.elements.UIButton(pygame.Rect(10,210,125,30),"New",manager,toolpanel,"Create new image"),
    'load': pygame_gui.elements.UIButton(pygame.Rect(10,250,125,30),"Load",manager,toolpanel,"Load image from a file"),
    'save': pygame_gui.elements.UIButton(pygame.Rect(10,290,125,30),"Save",manager,toolpanel,"Save image to a file",visible=0),
}

current_tool = "Pencil"

def handle_toolbar(event):
    if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == toolpanel_elements["toolpicker"]:
        current_tool = event.text
        print(current_tool)
    if event.type == pygame_gui.UI_BUTTON_PRESSED:
        if event.ui_element == toolpanel_elements['color1']:
            pygame_gui.windows.UIColourPickerDialog(pygame.Rect(0,0,640,480),manager, initial_colour=colors[0], window_title="Choose primary color...", object_id="color1")
        if event.ui_element == toolpanel_elements['color2']:
            pygame_gui.windows.UIColourPickerDialog(pygame.Rect(0,0,640,480),manager, initial_colour=colors[1], window_title="Choose secondary color...", object_id="color2")
            

def handle_windows(event):
    if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
        if event.ui_object_id == "savefile":
            pass
        if event.ui_object_id == "loadfile":
            pass
    if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
        print(event.colour)
        print(event.ui_object_id)
        if event.ui_object_id == "color1":
            colors[0] = event.colour
            toolpanel_elements["color1"].set_text(color_to_hexstring(colors[0]))
        if event.ui_object_id == "color2":
            colors[1] = event.colour
            toolpanel_elements["color2"].set_text(color_to_hexstring(colors[1]))

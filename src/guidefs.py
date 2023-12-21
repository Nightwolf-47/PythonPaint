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

newfile_window = None
newfile_input_elements = []

def get_supported_path(path):
    filename, extension = os.path.splitext(path)
    if extension in [".png",".jpg",".bmp",".jpeg"]:
        return path
    else:
        return filename + ".png"

def open_newfile_window():
    global newfile_window, newfile_input_elements
    newfile_window = pygame_gui.elements.UIWindow(pygame.Rect(0,0,200,250),manager,"Create new image",object_id="newfile")
    label1 = pygame_gui.elements.UILabel(pygame.Rect(20,10,125,20),"Width (1-9999)",manager,newfile_window)
    widthinput = pygame_gui.elements.UITextEntryLine(pygame.Rect(20,30,125,30),manager,newfile_window,object_id="widthinput")
    label2 = pygame_gui.elements.UILabel(pygame.Rect(20,70,125,20),"Height (1-9999)",manager,newfile_window)
    heightinput = pygame_gui.elements.UITextEntryLine(pygame.Rect(20,90,125,30),manager,newfile_window,object_id="heightinput")
    confirmbutton = pygame_gui.elements.UIButton(pygame.Rect(10,140,50,30),"Ok",manager,newfile_window,"Create new image",object_id="newfileconfirm")
    cancelbutton = pygame_gui.elements.UIButton(pygame.Rect(70,140,80,30),"Cancel",manager,newfile_window,"Go back to previous image",object_id="newfilecancel")
    widthinput.set_allowed_characters('numbers')
    widthinput.set_text_length_limit(4)
    widthinput.set_text("512")
    heightinput.set_allowed_characters('numbers')
    heightinput.set_text_length_limit(4)
    heightinput.set_text("512")
    newfile_input_elements = [widthinput,heightinput,confirmbutton,cancelbutton]
    

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
            open_newfile_window()
        elif event.ui_element == toolpanel_elements['load']:
            pygame_gui.windows.UIFileDialog(pygame.Rect(0,0,640,480),manager,"Load file...",{'.png','.jpg','.bmp','.jpeg'},os.path.curdir,object_id="loadfile")
        elif event.ui_element == toolpanel_elements['save']:
            pygame_gui.windows.UIFileDialog(pygame.Rect(0,0,640,480),manager,"Save file...",{'.png','.jpg','.bmp','.jpeg'},os.path.curdir,object_id="savefile")
        

def handle_newfile_window(event):
    if newfile_window != None:
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == newfile_input_elements[2]:
                imgx = newfile_input_elements[0].get_text()
                imgy = newfile_input_elements[1].get_text()
                imgx = int(imgx) if len(imgx) > 0 else 512
                imgy = int(imgy) if len(imgy) > 0 else 512
                paint.new_image(imgx,imgy)
                initialize_program(imgx,imgy)
                newfile_window.kill()
            elif event.ui_element == newfile_input_elements[3]:
                newfile_window.kill()
        if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
            try:
                result = max(int(event.text),1)
                event.ui_element.set_text(str(result))
            except:
                pass


def handle_windows(event):
    if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
        realpath = get_supported_path(event.text)
        if event.ui_object_id == "savefile":
            if paint.save_image(realpath):
                pygame_gui.windows.UIMessageWindow(pygame.Rect(0,0,400,180),f"File {os.path.basename(realpath)} saved successfully!",manager,window_title="Save File Success")
            else:
                pygame_gui.windows.UIMessageWindow(pygame.Rect(0,0,400,180),f"File {os.path.basename(realpath)} couldn't be saved!",manager,window_title="Save File Failure")
        if event.ui_object_id == "loadfile":
            load_image(event.text)
    if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
        if event.ui_object_id == "color1":
            colors[0] = event.colour
            toolpanel_elements["color1"].set_text(color_to_hexstring(colors[0]))
        if event.ui_object_id == "color2":
            colors[1] = event.colour
            toolpanel_elements["color2"].set_text(color_to_hexstring(colors[1]))

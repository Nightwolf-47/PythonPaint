import pygame
import math
from PIL import Image, ImageDraw, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

current_image = None
img_surface = None
image_scale = 1
rendered_imgsize = [640,480]
last_draw_point = None

colors = [pygame.Color(0,0,0), pygame.Color(255,255,255)]

current_tool = "Pencil"

brush_size = 1

def get_circle_topleftcorner(xy):
    half_brush_size = int(brush_size/2) if brush_size > 1 else 0
    return xy[0]-half_brush_size, xy[1]-half_brush_size

def get_image_scale():
    global image_scale
    imgx, imgy = current_image.size
    image_scale = math.ceil(max(min(640/imgx, 480/imgy), 1))
    rendered_imgsize[0] = int(imgx*image_scale)
    rendered_imgsize[1] = int(imgy*image_scale)
    print(image_scale)

def generate_image_from_pil():
    global img_surface
    img_surface = pygame.image.frombytes(current_image.tobytes(),current_image.size,current_image.mode)

def open_image(path):
    global current_image
    try:
        with Image.open(path) as im:
            current_image = Image.new("RGB",im.size,(colors[1].r,colors[1].g,colors[1].b))
            current_image.paste(im,(0,0),im.convert("RGBA"))
        generate_image_from_pil()
        get_image_scale()
        return current_image.size
    except Exception as e:
        print(e)
        return None


def save_image(path):
    if current_image != None:
        try:
            current_image.save(path)
            return True
        except:
            return False
    else:
        return False

def new_image(x,y):
    global current_image
    current_image = Image.new('RGB',(x,y))
    generate_image_from_pil()
    get_image_scale()

def flood_fill(pos,rgb):
    global last_draw_point
    last_draw_point = None
    if current_image == None:
        return
    ImageDraw.floodfill(current_image,pos,(*rgb,255),thresh=0)
    generate_image_from_pil()

def draw(pos,rgb):
    global last_draw_point
    if current_image == None:
        return
    imdraw = ImageDraw.Draw(current_image)
    bs = brush_size-1
    circlepos = get_circle_topleftcorner(pos)
    circlepos = [circlepos[0],circlepos[1],circlepos[0]+bs,circlepos[1]+bs]
    if last_draw_point:
        circleldp = get_circle_topleftcorner(last_draw_point)
        circleldp = [circleldp[0],circleldp[1],circleldp[0]+bs,circleldp[1]+bs]
        imdraw.ellipse(circleldp,rgb,rgb)
        imdraw.line([last_draw_point,pos],fill=rgb,width=brush_size+1 if brush_size > 1 else 1)
        imdraw.ellipse(circlepos,rgb,rgb)
    else:
        imdraw.ellipse(circlepos,rgb,rgb)
    last_draw_point = pos
    generate_image_from_pil()

from PIL import Image, ImageDraw, ImageTk
import random
from numpy import sort
import tkinter as tk
from tkinter import ttk

width = 1500
height = 1500
max_width = 400
road_width = 20
canvas = Image.new("RGBA",(width , height ), "green")
draw = ImageDraw.Draw(canvas)
batas = [(0,0)]
space = 20
building = [
    Image.open("bangunan/small-b.jpg").resize((20,20)), 
    Image.open("bangunan/small-b2.jpg").resize((20,20)), 
    Image.open("bangunan/large-building.jpg").resize((100,50)),
    Image.open("bangunan/large-building2.jpg").resize((100,50)), 
    Image.open("bangunan/large-building3.jpg").resize((100,50)), 
    Image.open("bangunan/building.jpeg").resize((50,30)),
    Image.open("bangunan/building2.jpg").resize((50,30)),
    Image.open("bangunan/building-eb.jpeg").resize((40,40)),
    Image.open("bangunan/house-b.jpg").resize((10,20)),
]

environment = [
    Image.open("properti/payung.jpeg").convert("RGBA").resize((40,40)),
    Image.open("properti/rumput1.jpeg").convert("RGBA").resize((20,20)),
    Image.open("properti/rumput2.jpg").convert("RGBA").resize((40,20)),
    Image.open("properti/pohon1.jpeg").convert("RGBA").resize((55,40)),
    Image.open("properti/pohon1.jpeg").convert("RGBA").resize((55,40)),
    Image.open("properti/batu.jpeg").convert("RGBA").resize((20,20)),
    Image.open("properti/nongki.jpeg").convert("RGBA").resize((30,30)),
]

def drawArea(awal, akhir, batAs, sisa):
    global building
    print(sisa , ": ", awal, akhir)
    awal = (awal[0], max(awal[1], batAs))
    xsort = sort([awal[0],akhir[0]])
    ysort = sort([awal[1],akhir[1]])
    if awal[0] < akhir[0] and awal[1] < akhir[1]: draw.rectangle(((awal[0]+1, awal[1]+1), (akhir[0]-1 , akhir[1]-1)), (60, 60, 60))
    awal = (awal[0] + 20 , awal[1]+20)
    akhir = (akhir[0] - 20 , akhir[1]-20)
    x = xsort[0] + 20
    y = ysort[0] + 20
    if awal[0] < akhir[0] and awal[1] < akhir[1]: draw.rectangle((awal,akhir), "green")
    while y <= ysort[1] - 60:
        while x <= xsort[1] : 
            gedung = [gedung for gedung in building if gedung.size[0] + x < xsort[1] - 20]
            if not gedung : break
            bangunan = random.choice(environment if y > ysort[0] + 20 and y <= ysort[1]-150 else gedung)
            if x + bangunan.size[0] >= xsort[1] -20 : break
            if y > ysort[0] + 20 and y < ysort[1]-150  : canvas.paste(bangunan, (x,(y + random.randint(0, 60-bangunan.size[1]))))
            else : canvas.paste(bangunan, (x,y if y <= ysort[1]-150 else ysort[1]-bangunan.size[1]-20))
            x += bangunan.size[0] + space
        y += 70
        x = xsort[0] + 20

def draw_dashed_line(draw, start_pos, end_pos, dash_length=10, gap_length=5, color="white"):
    """
    Draw a dashed line between start_pos and end_pos with specified dash and gap lengths.
    """
    x1, y1 = start_pos
    x2, y2 = end_pos
    total_length = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
    dashes = int(total_length / (dash_length + gap_length))
    
    for i in range(dashes):
        start_x = x1 + (x2 - x1) * (i * (dash_length + gap_length) / total_length)
        start_y = y1 + (y2 - y1) * (i * (dash_length + gap_length) / total_length)
        end_x = x1 + (x2 - x1) * ((i * (dash_length + gap_length) + dash_length) / total_length)
        end_y = y1 + (y2 - y1) * ((i * (dash_length + gap_length) + dash_length) / total_length)
        
        draw.line([(start_x, start_y), (end_x, end_y)], fill=color)

def makeArea(startPoint):
    global width, height, road_width, batas, draw
    print(startPoint)
    
    y = startPoint[1] + 200
    x = startPoint[0]
    tempX = 0
    tempY = 0
    limit_reached = 0
    tempAtas = []
    
    while y <= height and not limit_reached:
        tempX = 0
        if y >= height:
            limit_reached += 1
        
        while x <= width + 200:
            batAs, batEs = batas[-1][1], batas[-1][1]
            yey = random.choice([0, 100])
            tempAtas.append((x, y - yey))
            list_atas = []
            
            for atas in reversed(batas):
                if atas[0] > x:
                    batAs = atas[1]
                if atas[0] > tempX:
                    batEs = atas[1]
                if tempX < atas[0] < x:
                    list_atas.append(atas)
            
            if batEs < y - yey:
                if tempX < x and y <= height:
                    draw.rectangle(((tempX, y - yey), (x + 20, y - yey + 20)), "black")
                    draw_dashed_line(draw, (tempX + 20, y - yey + 10), (x, y - yey + 10), color="white")
                    draw.rectangle(((x, batAs), (x + 20, y - yey)), "black")
                    draw_dashed_line(draw, (x + 10, batAs + 20), (x + 10, y - yey), color="white")
                    if tempX < x and y <= height and tempX >= 20:
                        draw.rectangle(((tempX, batEs + 10), (tempX + 20, y - yey)), "black")
                        draw_dashed_line(draw, (tempX + 10, batEs + 20), (tempX + 10, y - yey), color="white")
                    
                drawArea((tempX + 20, batEs + 20), (x, y - yey), batAs + 20, list_atas)
            
            tempX = x
            tempY = batAs
            x += random.randint(2, 4) * 100
        
        y += 300
        tempAtas.append((tempX, tempY))
        
        if y > height:
            y = height
        
        batas = tempAtas
        tempAtas = []
        x = startPoint[0]

zoom_factor = 1.0
INITIAL_WIDTH = 800
INITIAL_HEIGHT = 800
viewport_x = 0
viewport_y = 0
viewport_width = 800
viewport_height = 800
new_map = None
scale = 1.0
canvas_width = 1500
canvas_height = 1500

def update_map():
    global draw, canvas, batas
    batas = [(0,0)]
    canvas = Image.new("RGBA",(width , height ), "green")
    draw = ImageDraw.Draw(canvas)
    makeArea((0,0))
    canvas.save("map.png")
    new_map  = canvas
    cropped_map = new_map.crop((viewport_x, viewport_y, viewport_x + viewport_width, viewport_y + viewport_height))
    resized_map = cropped_map.resize((INITIAL_WIDTH, INITIAL_HEIGHT))
    img_tk = ImageTk.PhotoImage(resized_map)
    map_label.config(image=img_tk)
    map_label.image = img_tk
    update()
    
def update():
    global canvas
    cropped_map = canvas.resize((int(canvas_width * scale), int(canvas_height * scale)))
    img_tk = ImageTk.PhotoImage(cropped_map)
    map_label.config(image=img_tk)
    map_label.image = img_tk
    resize_canvas()

def zoom_out():
    global scale
    scale /= 1.1
    update()

def zoom_in():
    global scale
    scale *= 1.1
    update()

def scroll(event):
    global viewport_x, viewport_y
    if event.delta > 0:
        if viewport_y > 0:
            viewport_y -= 10
    else:
        if viewport_y < height - viewport_height:
            viewport_y += 10
    update()


def on_scrollbar_press(event, direction):
    print(f"Scrollbar {direction} pressed at position ({event.x}, {event.y})") 

def resize_canvas():
    canvass.config(scrollregion=(0, 0, canvas_width*scale, canvas_height*scale))
    canvass.scale("all", 0, 0, scale, scale)
    canvass.config(width=canvas_width*scale, height=canvas_height*scale)

root = tk.Tk()
root.title("kota ku")
root.geometry("800x800")  
root.minsize(600, 400)  

root.bind("<MouseWheel>", scroll)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

canvass = tk.Canvas(frame, bg='white')
canvass.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

v_scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvass.yview)
v_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))

h_scroll = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvass.xview)
h_scroll.grid(row=1, column=0, sticky=(tk.W, tk.E))

canvass.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

v_scroll.bind("<ButtonPress-1>", lambda event: on_scrollbar_press(event, "vertical"))
h_scroll.bind("<ButtonPress-1>", lambda event: on_scrollbar_press(event, "horizontal"))

map_label = ttk.Label(canvass)
canvass.create_window((0, 0), window=map_label, anchor='nw')

generate_button = ttk.Button(root, text="Generate Map", command=update_map)
generate_button.grid(row=1, column=0, pady=10)

zoom_in_button = ttk.Button(root, text="Zoom In", command=zoom_in)
zoom_in_button.grid(row=2, column=0, pady=5)

zoom_out_button = ttk.Button(root, text="Zoom Out", command=zoom_out)
zoom_out_button.grid(row=3, column=0, pady=5)

def on_frame_configure(event):
    canvass.configure(scrollregion=canvass.bbox("all"))

frame.bind("<Configure>", on_frame_configure)

update_map()
root.mainloop()


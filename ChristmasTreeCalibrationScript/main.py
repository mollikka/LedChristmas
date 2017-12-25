from PIL import Image, ImageTk
from urllib import request
from statistics import mean
import tkinter

def get_image(url):

    download = request.urlopen(url)
    img = Image.open(download)
    img = img.rotate(270, expand=1)

    width = img.size[0]
    height = img.size[1]
    maxwidth = 1400
    maxheight = 700
    ratio = min(maxwidth/width, maxheight/height)

    img = img.resize((int(width*ratio), int(height*ratio)), Image.ANTIALIAS)
    return img

def find_maximum(image):

    point = [0,0]

    #http://stackoverflow.com/questions/8590234/capturing-x-y-coordinates-with-python-pil

    window = tkinter.Tk()

    canvas = tkinter.Canvas(window, width=image.size[0], height=image.size[1])
    canvas.pack()
    image_tk = ImageTk.PhotoImage(image)
    canvas.create_image(image.size[0]/2, image.size[1]/2, image=image_tk) 

    def callback(event):
        point[0],point[1] = event.x, event.y
        window.destroy()

    canvas.bind("<Button-1>", callback)
    tkinter.mainloop()

    return point

def scale_coordinates(coordinates):

    x_coords = [i[0] for i in coordinates]
    y_coords = [i[1] for i in coordinates]

    max_x = max(x_coords)
    max_y = max(y_coords)
    min_x = min(x_coords)
    min_y = min(y_coords)

    scaled_x = [(i-min_x)/(max_x-min_x)*100 for i in x_coords]
    scaled_y = [(i-min_y)/(max_y-min_y)*100 for i in y_coords]
    
    return zip(scaled_x, scaled_y)

def get_maximums_from_urls(urls):

    return [find_maximum(get_image(url)) for url in urls]

if __name__ == "__main__":
    
    urls = ["http://192.168.1.189/image.jpg",
            "http://192.168.1.166/image.jpg"]

    cam1_list = []
    cam2_list = []

    while True:

        cmd = input(">")
        
        if cmd == "":

            cam1,cam2 = get_maximums_from_urls(urls)

            cam1_list.append(cam1)
            cam2_list.append(cam2)
            
            print("cam1:", cam1)
            print("cam2:", cam2)

        if cmd == "undo":

            cam1_list.pop()
            cam2_list.pop()

        if cmd == "list":

            print("cam1:")
            for c in cam1_list:
                print(c)
            print()
            print("cam2:")
            for c in cam2_list:
                print(c)


        if cmd == "scale":

            cam1_scaled = scale_coordinates(cam1_list)
            cam2_scaled = scale_coordinates(cam2_list)
            
            print("cam1:")
            for c in cam1_scaled:
                print(c)
            print()
            print("cam2")
            for c in cam2_scaled:
                print(c)

        if cmd == "exit":
            break

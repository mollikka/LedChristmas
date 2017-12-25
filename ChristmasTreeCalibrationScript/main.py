from PIL import Image, ImageTk
from urllib import request
from statistics import mean
import tkinter
from serial import Serial

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
    
    return list(zip(scaled_x, scaled_y))

def get_maximums_from_urls(urls):

    return [find_maximum(get_image(url)) for url in urls]

def order_arduino_led_number(arduino_connection, number):

    while True:
        arduino_connection.write(bytes(str(number)+"\n","ascii"))
        return_message = ""
        str_in = arduino_connection.readline()
        return_message = str(str_in, 'ascii')
        if (return_message.strip() == '') or (int(return_message) != number):
            print("Communication error. Sent {} and read back as {}. Resending.".format(
                number,return_message))
        else:
            return

def write_out_coords(cam1_coords, cam2_coords):

    xcoord_file = open("XCOORD.txt","w")
    ycoord_file = open("YCOORD.txt","w")
    zcoord_file = open("ZCOORD.txt","w")

    x_list =  [i[0] for i in cam1_coords]
    y_list =  [i[0] for i in cam2_coords]
    z_list1 = [i[1] for i in cam1_coords]
    z_list2 = [i[1] for i in cam2_coords]

    z_list = [(z_list1[i] + z_list2[i]) /2 for i in range(len(z_list1))]
    print(z_list)

    xcoord_file.write("XCOORD["+str(len(x_list))+"] = {\n")
    for i in x_list:
        xcoord_file.write(str(i)+",\n")
    xcoord_file.write("};\n")

    ycoord_file.write("YCOORD["+str(len(y_list))+"] = {\n")
    for i in y_list:
        ycoord_file.write(str(i)+",\n")
    ycoord_file.write("};\n")

    zcoord_file.write("ZCOORD["+str(len(z_list))+"] = {\n")
    for i in z_list:
        zcoord_file.write(str(i)+",\n")
    zcoord_file.write("};\n")

    xcoord_file.close()
    ycoord_file.close()
    zcoord_file.close()

if __name__ == "__main__":
    
    urls = ["http://192.168.10.43/image.jpg",
            "http://192.168.10.35:8080/stream/live.jpg"]

    arduino_serial_address = "/dev/ttyACM0"

    serial_speed = 115200

    cam1_list = []
    cam2_list = []

    arduino_connection = Serial(arduino_serial_address, serial_speed, timeout=1)
        
    '''
    for i in range(150):
        print(i)
        order_arduino_led_number(arduino_connection, i)
        from time import sleep
        sleep(1)
    '''
    while True:

        order_arduino_led_number(arduino_connection, len(cam1_list))
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


        if cmd == "save":

            cam1_scaled = scale_coordinates(cam1_list)
            cam2_scaled = scale_coordinates(cam2_list)

            write_out_coords(cam1_scaled, cam2_scaled)

        if cmd == "exit":
            break

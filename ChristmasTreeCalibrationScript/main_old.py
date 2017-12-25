from PIL import Image
from urllib import request
from statistics import mean

def get_image(url):

    data = request.urlopen(url)
    img = Image.open(data)
    return img

def find_maximum(image):

    bw = image.convert('L')
    mini,maxi = bw.getextrema()
    width,height = image.size
    maximum_spots = [(x,y) for x in range(width) for y in range(height) if bw.getpixel((x,y)) == maxi]

    maximum_spots_x = [i[0] for i in maximum_spots]
    maximum_spots_y = [i[1] for i in maximum_spots]

    return mean(maximum_spots_x), mean(maximum_spots_y)

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
            "http://192.168.1.165/image.jpg"]

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

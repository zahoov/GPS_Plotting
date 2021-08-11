from PIL import Image

input_file_location = 1
output_file_location = 1

#this is currently set for a pi but just replace the directory with whatever yours is
workingDir = '/home/pi/GPS_Logging'

image1 = Image.open(workingDir + 'map.png')
image1.load()
im1 = Image.new("RGB", image1.size, (255, 255, 255))
im1.paste(image1, mask=image1.split()[3])
im1.save(workingDir + 'DrivingMap.pdf')

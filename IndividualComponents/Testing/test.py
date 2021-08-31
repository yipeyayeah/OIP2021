import os

directory = r'/home/pi/Desktop/OIP2021/IndividualComponents/Testing/TestImages'
for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        print(os.path.join(directory, filename))
    else:
        continue
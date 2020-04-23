import os

def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            return directory
    except OSError:
        print ('Khong the tao duoc thu muc!' +  directory)
        
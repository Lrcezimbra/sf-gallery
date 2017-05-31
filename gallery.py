import os
import tinify
from decouple import config

def main():
    tinify.key = config('TINYPNG_KEY')
    images_path = '/home/lucas/Pictures/8ª Corrida de São Jorge'
    new_images_path = '/home/lucas/Downloads/galeria'

    if not os.path.exists(new_images_path):
        os.mkdir(new_images_path)

    files = list(os.scandir(images_path))
    filespaths = [file.path for file in files]
    new_names = ['{:03d}.{}'.format(index+1, file.name[-3:])
                 for index, file in enumerate(files)]
    new_filepaths = [os.path.join(new_images_path, new_name)
                     for new_name in new_names]


    for filepath, new_filepath in zip(filespaths, new_filepaths):
        print(filepath, new_filepath)
        tinify.from_file(filepath)\
              .resize(method='scale',height=720)\
              .to_file(new_filepath)

    print(new_names)

if __name__ == '__main__':
    main()

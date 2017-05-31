import argparse
import os
import tinify
from decouple import config

def main(args):
    tinify.key = config('TINYPNG_KEY')
    images_srcpath = args.src
    output_path = args.output

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    files = list(os.scandir(images_srcpath))
    filespaths = [file.path for file in files]
    new_names = ['{:03d}.{}'.format(index+1, file.name[-3:])
                 for index, file in enumerate(files)]
    new_filepaths = [os.path.join(output_path, new_name)
                     for new_name in new_names]


    for filepath, new_filepath in zip(filespaths, new_filepaths):
        print(filepath, new_filepath)
        tinify.from_file(filepath)\
              .resize(method='scale',height=720)\
              .to_file(new_filepath)

    print(new_names)

def create_parser():
    parser = argparse.ArgumentParser(description='Resize and compress images for gallery.')
    parser.add_argument('src', help='path of source images')
    parser.add_argument('output', help='path to output processed images')
    return parser.parse_args()

if __name__ == '__main__':
    args = create_parser()
    main(args)

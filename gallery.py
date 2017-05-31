import argparse
import os
import tinify
from decouple import config

class Main():
    def __init__(self, args):
        tinify.key = config('TINYPNG_KEY')
        self.images_srcpath = args.src
        self.output_path = args.output

    def main(self):
        self._create_output_dir()
        src_output_filepaths = self._get_filespaths()
        self._resize_and_compress(src_output_filepaths)

    def _resize_and_compress(self, src_output_filepaths):
        for src_filepath, output_filepath in src_output_filepaths:
            print('{} ----> {}'.format(src_filepath, output_filepath))
            tinify.from_file(src_filepath)\
                  .resize(method='scale',height=720)\
                  .to_file(output_filepath)

    def _create_output_dir(self):
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

    def _get_srcfilepaths(self, src_files):
        return [file.path for file in src_files]

    def _get_output_filepaths(self, src_files):
        output_names = ['{:03d}.{}'.format(index+1, file.name[-3:])
                        for index, file in enumerate(src_files)]
        return [os.path.join(self.output_path, output_name)
                for output_name in output_names]

    def _get_filespaths(self):
        src_files = list(os.scandir(self.images_srcpath))
        src_filespaths = self._get_srcfilepaths(src_files)
        output_filepaths = self._get_output_filepaths(src_files)

        return zip(src_filespaths, output_filepaths)

def create_parser():
    parser = argparse.ArgumentParser(description='Resize and compress images for gallery.')
    parser.add_argument('src', help='path of source images')
    parser.add_argument('output', help='path to output processed images')
    return parser.parse_args()

if __name__ == '__main__':
    args = create_parser()
    Main(args).main()

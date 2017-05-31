import argparse
import os
import tinify
from decouple import config

class Main():
    def main(self, args):
        tinify.key = config('TINYPNG_KEY')
        images_srcpath = args.src
        output_path = args.output

        self._create_output_dir(output_path)
        src_output_filepaths = self._get_filespaths(images_srcpath, output_path)

        for src_filepath, output_filepath in src_output_filepaths:
            print('{} ----> {}'.format(src_filepath, output_filepath))
            tinify.from_file(src_filepath)\
                  .resize(method='scale',height=720)\
                  .to_file(output_filepath)

    def _create_output_dir(self, output_path):
        if not os.path.exists(output_path):
            os.mkdir(output_path)

    def _get_srcfilepaths(self, src_files):
        return [file.path for file in src_files]

    def _get_output_filepaths(self, src_files, output_path):
        output_names = ['{:03d}.{}'.format(index+1, file.name[-3:])
                        for index, file in enumerate(src_files)]
        return [os.path.join(output_path, output_name)
                for output_name in output_names]

    def _get_filespaths(self, images_srcpath, output_path):
        src_files = list(os.scandir(images_srcpath))
        src_filespaths = self._get_srcfilepaths(src_files)
        output_filepaths = self._get_output_filepaths(src_files, output_path)

        return zip(src_filespaths, output_filepaths)

def create_parser():
    parser = argparse.ArgumentParser(description='Resize and compress images for gallery.')
    parser.add_argument('src', help='path of source images')
    parser.add_argument('output', help='path to output processed images')
    return parser.parse_args()

if __name__ == '__main__':
    args = create_parser()
    Main().main(args)

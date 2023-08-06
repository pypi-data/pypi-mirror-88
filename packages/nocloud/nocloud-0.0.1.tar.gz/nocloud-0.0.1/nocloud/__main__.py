import argparse
import io
import pathlib
import sys

import pycdlib
import pyvhd

def __parse_args():
    parser = argparse.ArgumentParser(description="Generate a NoCloud disk image from a directory.")
    parser.add_argument(
            '-d',
            '--directory',
            type=str,
            default='.',
            help='Path containing files for disk image.'
    )
    parser.add_argument(
            '-t',
            '--type',
            type=str,
            default='raw',
            help='Type of image to generate (raw or vhd).'
    )
    parser.add_argument(
            '-o',
            '--output',
            type=pathlib.Path,
            help='Filename to write to.',
            required=True
    )
    return parser.parse_args()


def __generate_raw(directory):
    '''Return a file-like object containing the raw disk data for directory.'''
    root_path = pathlib.Path(directory).resolve()
    filenames = root_path.glob('**/*')

    iso = pycdlib.PyCdlib()
    iso.new(vol_ident='cidata', joliet=3, rock_ridge='1.09')
    for path in filenames:
        rel_filename = str(path)[len(str(root_path)):].lstrip('/')
        # Add directories.
        if path.is_dir():
            iso.add_directory(joliet_path='/%s' % rel_filename, rr_name='/%s' % rel_filename)
            continue

        # Add file
        iso.add_file(path, joliet_path='/%s' % rel_filename, rr_name='%s' % rel_filename)

    output = io.BytesIO()
    iso.write_fp(output)
    iso.close()
    output.seek(0)

    return output


def __to_vhd(data):
    '''Return bytes of vhd file.'''
    output_buffer = io.BytesIO()
    pyvhd.do_vhd_convert(data, output_buffer)
    output_buffer.seek(0)
    return output_buffer.read()



CONVERTER = {
    'raw': lambda infile: infile.read(),
    'vhd': __to_vhd,
}

if __name__ == '__main__':
    args = __parse_args()

    if args.type not in CONVERTER:
        print('Invalid type specified.')
        sys.exit(1)

    raw = __generate_raw(args.directory)
    converted = CONVERTER[args.type](raw)

    # Write file
    with open(args.output, 'wb') as output_file:
        output_file.write(converted)
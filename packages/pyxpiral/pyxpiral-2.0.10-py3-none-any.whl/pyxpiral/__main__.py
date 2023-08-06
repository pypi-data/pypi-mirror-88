#!/usr/bin/env python
"""
pyxpiral.py - Pseudo-DataMatrix (de)coder.
"""

import argparse
import operator
import math
import binascii
import sys
import struct
import numpy
from PIL import Image
from math import gcd
try:
    from pyxpiral import __version__
except:
    from __init__ import __version__


class Pyxpiral:
    """Turns any ascii string into a 2d bitmap + animated gif and vice-versa.
    """

    def __init__(self):
        pass

    @staticmethod
    def _get_bits_from_msg(message):
        return bin(
            int(binascii.hexlify(message if sys.version_info < (3, 0) else bytes(message, 'ascii')),
                base=16))[2:] + '1'

    @staticmethod
    def _get_dim(size):
        return int(math.ceil(math.sqrt(size)))

    @staticmethod
    def _get_offset(dim):
        return int(math.ceil((dim - 1) // 2))

    @staticmethod
    def _get_rgb_color(int_color):
        rgb_color = [k for k in struct.pack('>i', int_color)[1:]]
        if sys.version_info < (3, 0):
            rgb_color = [ord(k) for k in rgb_color]
        return numpy.array(rgb_color)

    @staticmethod
    def _array_to_image(msg_matrix):
        image = Image.fromarray(numpy.array(msg_matrix).astype('uint8'))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        return image

    @staticmethod
    def _image_to_array(image, downscale=10):
        image = image.resize([x // downscale for x in image.size], Image.NEAREST)
        return numpy.asarray(image, dtype="int32")

    @staticmethod
    def _array_to_bits(image_matrix, bg_color=0x00, bits_color=0xFFFFFF, step_size=1, ld_border=1):
        bg_color_rgb = Pyxpiral._get_rgb_color(bg_color)
        bits_color_rgb = Pyxpiral._get_rgb_color(bits_color)
        dim = len(image_matrix)-ld_border
        xpsize = int(math.pow(dim, 2))
        offset = Pyxpiral._get_offset(dim)
        offset_cur = [offset, offset + ld_border]
        bits = []
        for cur in Pyxpiral._get_cursor(xpsize, offset_cur, step_size):
            bits.append('0' if numpy.linalg.norm(image_matrix[cur[0]][cur[1]] - bg_color_rgb) <=
                        numpy.linalg.norm(image_matrix[cur[0]][cur[1]] - bits_color_rgb)
                        else '1')
        return ''.join(bits).rstrip('0')[:-1]

    @staticmethod
    def _bits_to_ascii(bits, encoding='ascii', errors='replace'):
        i = int(bits, 2)
        hex_string = '%x' % i
        k = len(hex_string)
        return binascii.unhexlify(hex_string.zfill(k + (k & 1))).decode(encoding, errors)

    @staticmethod
    def _get_cursor(xpiral_size, offset_cursor=None, step_size=1):
        cur = offset_cursor or [0, 0]
        refs = [1, 1]
        movs = [[step_size, 0], [0, step_size], [-step_size, 0], [0, -step_size]]
        i = 0
        j = 0
        k = 0
        while i < xpiral_size:
            yield cur
            cur = list(map(operator.add, cur, movs[j]))
            if k == 0:
                refs[j % 2] += 1
                j = (j + 1) % len(movs)
            k = (k + 1) % refs[j % 2]
            i += 1

    @staticmethod
    def _pixpiralize(bits, bg_color=0x00, bits_color=0xFFFFFF, step_size=1, ld_border=1):
        bg_color_rgb = Pyxpiral._get_rgb_color(bg_color)
        bits_color_rgb = Pyxpiral._get_rgb_color(bits_color)
        xpsize = len(bits)
        dim = Pyxpiral._get_dim(xpsize * step_size)
        bit_matrix = [[bg_color_rgb for _ in range(dim + ld_border)] for _ in
                      range(dim + ld_border)]
        offset = Pyxpiral._get_offset(dim)
        offset_cur = [offset, offset + ld_border]
        i = 0
        for cur in Pyxpiral._get_cursor(xpsize, offset_cur, step_size):
            bit_matrix[cur[0]][cur[1]] = bits_color_rgb if int(bits[i]) else bg_color_rgb
            i += 1
        return bit_matrix

    @staticmethod
    def encode(msg, upscale=10, colors=None, step_size=1, ld_border=1):
        """Encodes ascii message into BMP image.

        Args:
            msg (str): Message to encode.
            upscale (int, default=10): bit size in square pixels
            colors (list, default=[0x00, 0xFFFFFF]): (int) color for bit values 0, 1
            step_size (int, default=1): distance between consecutive bits
            ld_border (int, default=1): distance between consecutive bits

        Returns:
            (PIL.Image.Image): An image object from Pillow library
        """
        if not colors:
            bg_color, bits_color = 0x00, 0xFFFFFF
        else:
            bg_color, bits_color = colors[0], colors[1]
        bits = Pyxpiral._get_bits_from_msg(msg)
        msg_matrix = Pyxpiral._pixpiralize(
            bits,
            bg_color=bg_color,
            bits_color=bits_color,
            step_size=step_size,
            ld_border=ld_border
        )
        image = Pyxpiral._array_to_image(msg_matrix)
        return image.resize([x * upscale for x in image.size], Image.NEAREST)

    @staticmethod
    def encode_fractal(msg, upscale=10, colors=None, step_size=1, rotation_step=1):
        """Encodes ascii message into GIF animated image sequence.

        Args:
            msg (str): Message to encode.
            upscale (int, default=10): bit size in square pixels
            colors (list, default=[0x00, 0xFFFFFF]): (int) color for bit values 0, 1
            step_size (int, default=1): distance between consecutive bits
            rotation_step (int, default=1): bits rotated per gif frame

        Returns:
            (list): A list of PIL.Image.Image objects from Pillow library
        """
        if not colors:
            bg_color, bits_color = 0x00, 0xFFFFFF
        else:
            bg_color, bits_color = colors[0], colors[1]
        bits = Pyxpiral._get_bits_from_msg(msg)
        num_rotations = int(len(bits) // gcd(len(bits), rotation_step))
        msg_img_seq = []
        ld_border = 1
        for _ in range(num_rotations):
            image = Pyxpiral._array_to_image(
                Pyxpiral._pixpiralize(
                    bits,
                    bg_color=bg_color,
                    bits_color=bits_color,
                    step_size=step_size,
                    ld_border=ld_border
                )
            )
            image = image.resize([x * upscale for x in image.size], Image.NEAREST)
            msg_img_seq.append(image)
            bits = bits[-rotation_step - 1:-1] + bits[:-rotation_step - 1] + '1'
        return msg_img_seq

    @staticmethod
    def decode(image, downscale=10, colors=None, step_size=1):
        """Decodes ascii message from BMP image.

        Args:
            image (PIL.Image.Image): source BMP image.
            downscale (int, default=10): bit size in square pixels
            colors (list, default=[0x00, 0xFFFFFF]): (int) color for bit values 0, 1
            step_size (int, default=1): distance between consecutive bits

        Returns:
            (str): Decoded ascii string message
        """
        if not colors:
            bg_color, bits_color = 0x00, 0xFFFFFF
        else:
            bg_color, bits_color = colors[0], colors[1]
        image_array = Pyxpiral._image_to_array(image, downscale=downscale)
        bits = Pyxpiral._array_to_bits(
            image_array,
            bg_color=bg_color,
            bits_color=bits_color,
            step_size=step_size
        )
        return Pyxpiral._bits_to_ascii(bits)


def _auto_int(x):
    return int(x, 0)


def main(argv):
    """Processes the program input arguments for turning any ascii string into a 2d bitmap or gif
    and vice-versa.

        Args:
            argv (list): list of str containing the program input arguments.
    """

    parser = argparse.ArgumentParser(
        description='Pseudo-DataMatrix (de)coder with no practical use. Turns any ascii string' +
        'into a 2d bitmap + animated gif and vice-versa.')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--encode', help='message to encode')
    group.add_argument('-d', '--decode', default=False, type=argparse.FileType('rb'),
                       help='image to decode')
    group.add_argument('-v', '--version', help='print version and exit', action='store_true')

    parser.add_argument('-S', '--scale', default=10, type=int,
                        help='bit size in square pixels, default=10')
    parser.add_argument('-b', '--bg-color', default=0x00, type=_auto_int,
                        help='bit color for value 0, default=0x00')
    parser.add_argument('-B', '--bits-color', default=0xFFFFFF, type=_auto_int,
                        help='bit color for value 1, default=0xFFFFFF')
    parser.add_argument('-s', '--step-size', default=1, type=int,
                        help='distance between consecutive bits, default=1')
    parser.add_argument('-r', '--rotation-step', default=1, type=int,
                        help='bits rotated per gif frame, default=1')
    parser.add_argument('-f', '--frame-duration', default=100, type=int,
                        help='frame duration in ms, default=100')
    parser.add_argument('-l', '--loops', default=0, type=int,
                        help='number of gif loops (0=infinite), default=0')

    parser.add_argument('-o', '--output-filename', default=None, type=argparse.FileType('wb'),
                        help='output filename (.gif will be appended on gif generation)')

    args = parser.parse_args(argv[1:])

    if args.version:
        print("pyxpiral version "+__version__)
        return

    # Pyxpiral is static, instance is not required.
    ppl = Pyxpiral()

    if args.decode:
        image = Image.open(args.decode)
        image.load()
        msg = ppl.decode(
            image,
            downscale=args.scale,
            colors=[args.bg_color, args.bits_color],
            step_size=args.step_size
        )
        print(msg)
        return

    if not args.output_filename:
        args.output_filename = open('output.bmp', 'wb')

    image = ppl.encode(
        args.encode,
        upscale=args.scale,
        colors=[args.bg_color, args.bits_color],
        step_size=args.step_size
    )

    image.save(args.output_filename.name, format='BMP')

    msg_img_seq = ppl.encode_fractal(
        args.encode,
        upscale=args.scale,
        colors=[
            args.bg_color,
            args.bits_color
        ],
        step_size=args.step_size,
        rotation_step=args.rotation_step
    )

    msg_img_seq[0].save(
        args.output_filename.name + '.gif',
        save_all=True,
        append_images=msg_img_seq[1:],
        duration=args.frame_duration,
        loop=args.loops
    )

    print('Generated ' + args.output_filename.name + ' and ' + args.output_filename.name + '.gif')


if __name__ == "__main__":
    main(sys.argv)

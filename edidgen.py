#!/usr/bin/env python3

# Usage: ./edidgen.py out.bin 27e6 1440 40 118 118 240 3 4 16 True

import numpy as np
import sys
import subprocess
import ast


def add_detailed(arr, pixel_clock, hactive, hfp, hsync, hbp, vactive, vfp, vsync, vbp, interlace):
    pixel_clock = int(pixel_clock) // (10 * 1000)
    hblank = hfp + hsync + hbp
    vblank = vfp + vsync + vbp

    arr[0] = pixel_clock & 0xff
    arr[1] = pixel_clock >> 8
    arr[2] = hactive & 0xff
    arr[3] = hblank & 0xff
    arr[4] = (((hactive >> 8) & 0xf) << 4) | ((hblank >> 8) & 0xf)
    arr[5] = vactive & 0xff
    arr[6] = vblank & 0xff
    arr[7] = (((vactive >> 8) & 0xf) << 4) | ((vblank >> 8) & 0xf)
    arr[8] = hfp & 0xff
    arr[9] = hsync & 0xff
    arr[10] = ((vfp & 0xf) << 4) | (vsync & 0xf)
    arr[11] = (((hfp>>8)&3) << 6) | (((hsync>>8)&3) << 4) | (((vfp>>8)&3)<<2) | ((vsync>>8)&2)
    arr[17] = ((1 if interlace else 0) << 7) | (3 << 3)


def main():
    buffer = np.zeros((0x80, ), dtype=np.uint8)
    buffer[1:7] = 0xff

    buffer[16] = 0xff

    buffer[17] = (2024 - 1990)

    buffer[18] = 1
    buffer[19] = 4

    buffer[20] = (1<<7) | (2 << 4) | 1

    buffer[38:38+16] = 1

    args = tuple(ast.literal_eval(x) for x in sys.argv[2:])
    add_detailed(buffer[54:], *args)

    buffer[-1] = 256 - (int(np.sum(buffer[:-1])) & 0xff)

    buffer.tofile(sys.argv[1])
    subprocess.run(['edid-decode', sys.argv[1]])


    print("NTSC timings in usec should be 52.6, 1.5, 4.7, 4.7, total 63.5:")

    print(list(1e6 * x / args[0] for x in args[1:5]))
    print("Total:", 1e6 * sum(args[1:5]) / args[0])
if __name__ == '__main__':
    main()

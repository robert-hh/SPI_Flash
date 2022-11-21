# The MIT License (MIT)
#
# Copyright (c) 2016 Paul Sokolovsky
# Copyright (c) 2022 Robert Hammelrath
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

SECTOR_SIZE = const(4096)


class FlashBdev:
    def __init__(self, flash, sectorsize=SECTOR_SIZE):
        self.flash = flash
        self.sectorsize = sectorsize

    def readblocks(self, n, buf, offset=0):
        self.flash.readblock(n * self.sectorsize + offset, buf)

    def writeblocks(self, n, buf, offset=0):
        if offset == 0:
            self.flash.erase(n * self.sectorsize)
        self.flash.writeblock(n * self.sectorsize + offset, buf)

    def ioctl(self, op, arg):
        if op == 4:  # MP_BLOCKDEV_IOCTL_BLOCK_COUNT
            return self.flash.getsize() // self.sectorsize
        if op == 5:  # MP_BLOCKDEV_IOCTL_BLOCK_SIZE
            return self.sectorsize
        if op == 6:  # MP_BLOCKDEV_IOCTL_BLOCK_ERASE
            self.flash.erase(arg * self.sectorsize)
            return 0

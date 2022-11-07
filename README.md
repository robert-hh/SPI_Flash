# SPI Flash Block Device Driver.

This is a minimal block device driver to use a SPI connected flash
device for a MicroPython file system. The focus of that driver is
small size and simplicity, not speed. Nevertheless, it works reasonably
fast.

Constructor:

bdev = FlashBdev(spi, cs [addr4b])

spi has to b a SPI object, cs must be a Pin object of the cs pin. If
addr4b is True, a 4 byte addressing mode is used for the flash, otherwise
3 byte addresses are used, which are sufficient up to a flash size of
16 MByte.

The driver was tested with LittleFS Version 1 and 2, and also with a FAT
file system. The latter is NOT recommended.

Examples:

```
# Using HARD spi
import os
from flashbdev import FlashBdev
from machine import SPI, Pin

spi=SPI(5, sck=Pin("FLASH_SCK"), mosi=Pin("FLASH_MOSI"), miso=Pin("FLASH_MISO"), baudrate=8_000_000)
cs = Pin("FLASH_CS", Pin.OUT, value=1)

flash=FlashBdev(spi, cs)
try:
    vfs = os.VfsLfs1(flash, progsize=256)
except OSError as e:
    print("Mount failed with error", e)
    print("Recreate the file system")
    os.VfsLfs1.mkfs(flash, progsize=256)
    vfs = os.VfsLfs1(flash, progsize=256)

os.mount(vfs, "/flash")
os.chdir("/flash")
```

```
# Example using SoftSPI with a QSPI chip.
import os
from flashbdev import FlashBdev
from machine import SoftSPI, Pin

wp=Pin("FLASH_WP", Pin.OUT, value=1)
hold=Pin("FLASH_HOLD", Pin.OUT, value=1)
cs = Pin("FLASH_CS", Pin.OUT, value=1)
spi=SoftSPI(sck=Pin("FLASH_SCK"), mosi=Pin("FLASH_MOSI"), miso=Pin("FLASH_MISO"), baudrate=2_000_000)


flash=FlashBdev(spi, cs)
try:
    vfs = os.VfsLfs2(flash)
except OSError as e:
    print("Mount failed with error", e)
    print("Recreate the file system")
    os.VfsLfs2.mkfs(flash)
    vfs = os.VfsLfs2(flash)

os.mount(vfs, "/flash")
os.chdir("/flash")
```
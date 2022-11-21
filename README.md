# SPI Block Device Driver.

This is a combination of a raw SPI flash driver and a 
minimal block device driver to use a SPI connected flash
device for a MicroPython file system. The focus of that driver is
small size and simplicity, not speed. Nevertheless, it works reasonably
fast.

Constructor:

flash = SPIflash(spi, cs, *, addr4b=False, pagesize=256)

spi has to b a SPI object, cs must be a Pin object of the cs pin. If
addr4b is True, a 4 byte addressing mode is used for the flash, otherwise
3 byte addresses are used, which are sufficient up to a flash size of
16 MByte. 

The optional parameter pagesizeallow using devices with
non-standard values for this property.

bdev = FlashBdev(flash , *, sectorsize=4096)

flash is a SPIflash object created e.g. from spiflash.py.
The optional parameter sectorsize allow using devices with a
non-standard values for this property.

The drivers were tested with LittleFS Version 1 and 2, and also with a FAT
file system. The latter is NOT recommended. When using the driver with
SoftSPI, select LFS1 as file system. That is less space efficient, but faster.
The Lfs `progsize` parameter must not be less than 128.

Examples:

```
# Using HARD spi
import os
from flashbdev import FlashBdev
from spiflash import SPIflash
from machine import SPI, Pin

spi=SPI(0, sck=Pin("FLASH_SCK"), mosi=Pin("FLASH_MOSI"), miso=Pin("FLASH_MISO"), baudrate=12_000_000)
cs = Pin("FLASH_CS", Pin.OUT, value=1)

flash=FlashBdev(SPIflash(spi, cs))
try:
    vfs = os.VfsLfs1(flash, progsize=256)
except OSError as e:
    print("Mount failed with error", e)
    print("Recreate the file system")
    os.VfsLfs1.mkfs(flash, progsize=256)
    vfs = os.VfsLfs1(flash, progsize=256)

os.mount(vfs, "/flash")
```

```
# Example using SoftSPI with a QSPI chip.
import os
from flashbdev import FlashBdev
from spiflash import SPIflash
from machine import SPI, Pin

wp = Pin("PA10", Pin.OUT, value=1)
hold = Pin("PA11", Pin.OUT, value=1)
cs = Pin("PB11", Pin.OUT, value=1)
spi = SoftSPI(sck="PB10", mosi="PA08", miso="PA09", baudrate=2_000_000)

flash=FlashBdev(SPIflash(spi, cs))
try:
    vfs = os.VfsLfs1(flash, progsize=256)
except OSError as e:
    print("Mount failed with error", e)
    print("Recreate the file system")
    os.VfsLfs1.mkfs(flash, progsize=256)
    vfs = os.VfsLfs1(flash, progsize=256)

os.mount(vfs, "/flash")
```
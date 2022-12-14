# SPI Block Device Driver.

This is a combination of a raw SPI flash driver and a 
minimal block device driver to use a SPI connected flash
device for a MicroPython file system. The focus of that driver is
small size and simplicity, not speed. Nevertheless, it works 
reasonably fast. It shall be used with a VFS file system, which
takes care of only writing to erased areas.
A more generic NV memory driver can be found at
https://github.com/peterhinch/micropython_eeprom, which supports
different types of memory, any write sizes and spanning the memory
space over multiple chips.


## Constructors:

### flash = SPIflash(spi, cs, *, addr4b=False, size=None, pagesize=256, sectorsize=4096)

spi has to b a SPI object, cs must be a Pin object of the cs pin. If
addr4b is True, a 4 byte addressing mode is used for the flash, otherwise
3 byte addresses are used, which are sufficient up to a flash size of
16 MByte. 

The optional parameters size, pagesize and sectorsize allow using devices with
non-standard or non-detectable values for these properties.

### bdev = FlashBdev(flash )

flash is a SPIflash object created e.g. from spiflash.py.

The drivers were tested with LittleFS Version 1 and 2, and also with a FAT
file system. The latter is NOT recommended. When using the driver with
SoftSPI, select LFS1 as file system. That is less space efficient, but faster.
The Lfs `progsize` parameter must not be less than 128.

##  SPIflash Methods:

### flash.flash_read(addr, buffer)

Read data from addres into the buffer. The amount of data is defined by the buffer
size.

### flash.flash_write(addr, buffer)

Write data from the buffer at the address. The amount of data is defined by the buffer
size. The data is written in multiples of up to a page size, such that a single
write does not cross a page boundary.

### flash.flash_erase(addr)

Erase the sector at addr.


### flash.flash_size()

Return the total size of the flash as bytes. . This information is required by a file
system block device driver.

### flash.flash_sectorsize()

Return the size of a sector. This information is required by a file system block device driver.


## Examples:

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
    print("Recreate the file system")  # Previous content is lost!
    os.VfsLfs1.mkfs(flash, progsize=256)
    vfs = os.VfsLfs1(flash, progsize=256)

os.mount(vfs, "/flash")
```

```
# Example using SoftSPI with a QSPI device.
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
    print("Recreate the file system")  # Previous content is lost!
    os.VfsLfs1.mkfs(flash, progsize=256)
    vfs = os.VfsLfs1(flash, progsize=256)

os.mount(vfs, "/flash")
```
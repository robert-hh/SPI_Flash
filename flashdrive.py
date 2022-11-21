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
os.chdir("/flash")

import os
from flashbdev import FlashBdev
from spiflash import SPIflash
from machine import SPI, Pin

spi=SPI(0, sck="FLASH_SCK", mosi="FLASH_MOSI", miso="FLASH_MISO", baudrate=24_000_000)
cs = Pin("FLASH_CS", Pin.OUT, value=1)

flash=FlashBdev(SPIflash(spi, cs))
try:
    vfs = os.VfsLfs1(flash)
except OSError as e:
    print("Mount failed with error", e)
    print("Recreate the file system")
    os.VfsLfs1.mkfs(flash)
    vfs = os.VfsLfs1(flash)

os.mount(vfs, "/flash")
os.chdir("/flash")

# TI MSP430 Emulator: development platform for [PlatformIO](http://platformio.org)

This is a clone of PlatformIO MSP430 platform, except uploader is replaced with software emulator. Emulator is only available for MSP-EXP430G2553LP board.


MSP430 microcontrollers (MCUs) from Texas Instruments (TI) are 16-bit, RISC-based, mixed-signal processors designed for ultra-low power. These MCUs offer the lowest power consumption and the perfect mix of integrated peripherals for thousands of applications.

* [Home](http://platformio.org/platforms/timsp430) (home page in PlatformIO Platform Registry)
* [Documentation](http://docs.platformio.org/page/platforms/timsp430.html) (advanced usage, packages, boards, frameworks, etc.)
* [Emulator](https://github.com/zceemja/msp430emu) (emulator source code, list of implemented features)

# Usage

1. [Install PlatformIO](http://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](http://docs.platformio.org/page/projectconf.html) file:

```ini
[env:emulator]
platform = https://github.com/platformio/platform-timsp430.git
board = lpmsp430g2553
framework = arduino
...
```
3. Upload code. Upon uploading, PlatformIO will open emulator program.

# Configuration

Please navigate to [documentation](http://docs.platformio.org/page/platforms/timsp430.html).


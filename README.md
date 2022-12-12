# iRacing leds 

This is a small application allows you to visualise live telemetry data from iRacing on
some Yoctopuce devices. Shifting leds can be mapped on Yocto-Color-V2 led, and current 
gear can be displayed on a Yocto-MaxiDisplay

For more details, see [our blog article](https://www.yoctopuce.com)

## Requirement
- [Python 3.7+](https://www.python.org/downloads/)
- [Python iRacing SDK](https://github.com/kutu/pyirsdk)
- [Yoctopuce library for Python](https://github.com/yoctopuce/yoctolib_python)
- A [Yocto-Color-V2](https://www.yoctopuce.com/EN/products/modules-de-commande-usb/yocto-color-v2) for shifting leds
- A [Yocto-MaxiDisplay](https://www.yoctopuce.com/EN/products/ecrans-usb/yocto-maxidisplay) for current gear info

## Installation

In order the work the application require Yoctopuce library and iRacing SDK, which can
be installed using pip:

```
  pip install pyirsdk
  pip install yoctopuce
```

## Disclaimer

Yoctoupce is not affiliated with or supported by iRacing.com Motorsport Simulations.


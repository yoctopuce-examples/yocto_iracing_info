# Yoctopuce iRacing Info

This is a small application allows you to visualise live telemetry data from iRacing on
some Yoctopuce devices. Shifting leds can be mapped on Yocto-Color-V2 led, and current 
gear can be displayed on a Yocto-MaxiDisplay

For more details, see [our blog article](https://www.yoctopuce.com/EN/article/using-yoctopuce-modules-with-the-iracing-game)

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

## Execution

```
python yocto_iracing_info.py -l 40 -n 8
```
Note : By default the application use Yocopuce devices connected by USB, but you can specify a remote
hostname/IP with ``-r`` option. 

```
options:
  -h, --help            show this help message and exit
  -r REMOTEHUB, --remoteHub REMOTEHUB
                        Uses remote IP devices (or VirtalHub), instead of local USB.
  -n NB_LEDS, --nb_leds NB_LEDS
                        The number of Led connected to the Yocto-Color-V2
  -l LUMINOSITY, --luminosity LUMINOSITY
                        The luminosity of the leds (0..100)
```


## Disclaimer

Yoctopuce is not affiliated with or supported by iRacing.com Motorsport Simulations.


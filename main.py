#!python3
import sys

import irsdk

import irsdk2
from yoctopuce.yocto_api import *
from yoctopuce.yocto_display import *
from yoctopuce.yocto_colorledcluster import *


# ir = irsdk2.IRSDK()
##ir.startup()
def run():
    errmsg = YRefParam()
    if YAPI.RegisterHub("localhost", errmsg) != YAPI.SUCCESS:
        sys.exit("init error :" + errmsg.value)

        # retreive any RGB led
    led_cluster = YColorLedCluster.FirstColorLedCluster()
    disp = YDisplay.FirstDisplay()
    if led_cluster is None and disp is None:
        sys.exit('No module connected')

    if disp is not None:
        # display clean up
        disp.resetAll()

        # retreive the display size
        w = disp.get_displayWidth()
        h = disp.get_displayHeight()

        # retreive the first layer
        l0 = disp.get_displayLayer(0)

    nb_leds = 8
    led_cluster.set_activeLedCount(nb_leds)
    default_led_colors = []
    luminosity = 0x20
    green_hue = 0x55
    red_hue = 0x00
    for i in range(0, nb_leds):
        hue = round(((nb_leds - 1) - i) / (nb_leds - 1) * green_hue)
        color_hsl = (hue << 16) + 0xff00 + luminosity
        print("Led %d is 0x%x" % (i, color_hsl))
        default_led_colors.append(color_hsl)
        led_cluster.set_hslColor(i, 1, default_led_colors[i])

    min = ir['DriverInfo']['DriverCarSLFirstRPM']
    opt = ir['DriverInfo']['DriverCarSLShiftRPM']
    max = ir['DriverInfo']['DriverCarSLLastRPM']
    red = ir['DriverInfo']['DriverCarSLBlinkRPM']

    print("RPM: min=%d opt=%d max=%d red=%d" % (min, opt, max, red))
    last_led_color = default_led_colors[:]
    while True:
        rpm = ir['RPM']
        led_colors = [0] * nb_leds
        if min < rpm <= max:
            if opt < rpm:
                led_colors = [0x40FF00 + luminosity] * nb_leds
            else:
                nb_leds_on = round((rpm - min) * nb_leds / (max - min))
                for i in range(0, nb_leds_on):
                    led_colors[i] = default_led_colors[i]
        elif rpm > max:
            led_colors = [0xff00 + luminosity] * nb_leds
        if last_led_color != led_colors:
            led_cluster.set_hslColorArray(0, led_colors)
        last_led_color = led_colors[:]

        if disp is not None:
            l0.clear()
            l0.drawText(w / 2, h / 3, YDisplayLayer.ALIGN.CENTER, "%d" % rpm)
            l0.drawText(w / 2, h * 2 / 3, YDisplayLayer.ALIGN.CENTER, "%f" % ir['ShiftIndicatorPct'])


# this is our State class, with some helpful variables
class State:
    ir_connected = False
    last_car_setup_tick = -1


# here we check if we are connected to iracing
# so we can retrieve some data
def check_iracing():
    if state.ir_connected and not (ir.is_initialized and ir.is_connected):
        state.ir_connected = False
        # don't forget to reset your State variables
        state.last_car_setup_tick = -1
        # we are shutting down ir library (clearing all internal variables)
        ir.shutdown()
        print('irsdk disconnected')
    elif not state.ir_connected and ir.startup() and ir.is_initialized and ir.is_connected:
        state.ir_connected = True
        print('irsdk connected')


if __name__ == '__main__':
    # initializing ir and state
    ir = irsdk.IRSDK()
    state = State()

    try:
        # infinite loop
        while True:
            # check if we are connected to iracing
            check_iracing()
            # if we are, then process data
            if state.ir_connected:
                run()
            # sleep for 1 second
            # maximum you can use is 1/60
            # cause iracing updates data with 60 fps
            time.sleep(1)
    except KeyboardInterrupt:
        # press ctrl+c to exit
        pass

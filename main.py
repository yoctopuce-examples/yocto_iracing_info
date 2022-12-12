#!python3

import irsdk

from yoctopuce.yocto_display import *
from yoctopuce.yocto_colorledcluster import *


class IRacingLed:
    def __init__(self):
        self.display_w = 1
        self.display_h = 1
        self.ir_connected = False
        self.last_car_setup_tick = -1
        self.ir = irsdk.IRSDK()
        self.luminosity = 0x80
        self.nb_leds = 2
        self.ledCluster = None
        self.display = None
        self.luminosity = 0x20
        self.default_led_colors = []
        self.last_led_color = []
        self.layer0 = None
        self.lastGear = 'N'

        errmsg = YRefParam()
        err = YAPI.RegisterHub("usb", errmsg)
        if err != YAPI.SUCCESS:
            if err == YAPI.DOUBLE_ACCES:
                # usb access is probably already taken by VirtualHub
                # try to access Yoctopuce devices through VirtualHub
                err = YAPI.RegisterHub("usb", errmsg)
            if err != YAPI.SUCCESS:
                sys.exit("Unable to register hub :" + errmsg.value)
        YAPI.RegisterDeviceArrivalCallback(self.deviceArrival)
        YAPI.RegisterDeviceRemovalCallback(self.deviceRemoval)

    def deviceArrival(self, m: YModule):
        serial = m.get_serialNumber()
        print('Device arrival : ' + serial)
        if m.get_productName() == "Yocto-Color-V2":
            self.ledCluster = YColorLedCluster.FindColorLedCluster(serial + ".colorLedCluster")
            self.configure_leds()
        if m.get_productName().startswith("Yocto-MaxiDisplay"):
            self.display = YDisplay.FindDisplay(serial + ".display")
            self.configure_display()

    def deviceRemoval(self, m):
        serial = m.get_serialNumber()
        print('Device removal : ' + serial)
        if self.ledCluster is not None and serial == self.ledCluster.get_serialNumber():
            self.ledCluster = None
        if self.display is not None and serial == self.display.get_serialNumber():
            self.display = None

    def loop(self):
        # infinite loop
        while True:
            # check if we are connected to iracing
            if self.ir_connected and not (self.ir.is_initialized and self.ir.is_connected):
                self.ir_connected = False
                # don't forget to reset your State variables
                self.last_car_setup_tick = -1
                # we are shutting down ir library (clearing all internal variables)
                self.ir.shutdown()
                print('irsdk disconnected')
            elif not self.ir_connected and self.ir.startup() and self.ir.is_initialized and self.ir.is_connected:
                self.ir_connected = True
                print('irsdk connected')

            # if we are, then process data
            if self.ir_connected:
                self.refresh()
            # Check for Yoctopuce devices arrival or removal
            YAPI.UpdateDeviceList()

            # sleep for 1 second
            # maximum you can use is 1/60
            # cause iracing updates data with 60 fps
            YAPI.Sleep(16)

    def refresh(self):
        if self.ledCluster is not None:
            # retrieve any RGB leds
            min = self.ir['DriverInfo']['DriverCarSLFirstRPM']
            opt = self.ir['DriverInfo']['DriverCarSLShiftRPM']
            max = self.ir['DriverInfo']['DriverCarSLLastRPM']
            rpm = self.ir['RPM']
            # init all led to black
            led_colors = [0] * self.nb_leds
            if min < rpm <= max:
                if opt < rpm:
                    # optimum change rpm -> set all led to white
                    led_colors = [0x40FF00 + self.luminosity] * self.nb_leds
                else:
                    # light leds according the rpm
                    nb_leds_on = round((rpm - min) * self.nb_leds / (max - min))
                    for i in range(0, nb_leds_on):
                        led_colors[i] = self.default_led_colors[i]
            elif rpm > max:
                # rpm is too high -> set all led to red
                led_colors = [0xff00 + self.luminosity] * self.nb_leds
            if self.last_led_color != led_colors:
                self.ledCluster.set_hslColorArray(0, led_colors)
            self.last_led_color = led_colors[:]

        if self.display is not None:
            gear_char = 'X'
            gear = self.ir['Gear']
            if gear:
                if gear < 0:
                    gear_char = 'R'
                elif gear == 0:
                    gear_char = 'N'
                else:
                    gear_char = "%d" % gear
            if gear_char != self.lastGear:
                self.layer0.clear()
                self.layer0.drawText(self.display_w / 2, self.display_h / 2, YDisplayLayer.ALIGN.CENTER, gear_char)
                self.lastGear = gear_char

    def configure_leds(self):
        self.ledCluster.set_activeLedCount(self.nb_leds)
        self.default_led_colors = []
        green_hue = 0x55
        for i in range(0, self.nb_leds):
            hue = round(((self.nb_leds - 1) - i) / (self.nb_leds - 1) * green_hue)
            color_hsl = (hue << 16) + 0xff00 + self.luminosity
            # print("Led %d is 0x%x" % (i, color_hsl))
            self.default_led_colors.append(color_hsl)

    def configure_display(self):
        # display clean up
        self.display.resetAll()
        # retrieve the display size
        self.display_w = self.display.get_displayWidth()
        self.display_h = self.display.get_displayHeight()
        # retrieve the first layer
        self.layer0 = self.display.get_displayLayer(0)


if __name__ == '__main__':
    # initializing ir and state
    i_racing_led = IRacingLed()
    try:
        i_racing_led.loop()
    except KeyboardInterrupt:
        # press ctrl+c to exit
        pass

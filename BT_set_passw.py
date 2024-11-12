import RIS_usb_class
ris = RIS_usb_class.RIS_usb('COM8', 1)
ris.read_EXT_voltage()
ris.reset()
ris.set_BT_key('000000')
ris.read_pattern()
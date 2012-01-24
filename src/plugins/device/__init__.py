from pluginmgr import Device

import sys
import os.path
try:
    import dbus
    import dbus.mainloop.qt
except ImportError:
    dbus = None
from PyQt4 import QtCore

__drivers_path = os.path.join(os.path.dirname(__file__), '/drivers')

class DeviceDriver(object):
    """Base device driver class.
       All drivers should extend this class."""
    def __init__(self, device):
        pass

    def mount(self):
        pass

    def umount(self):
        pass

if dbus:
    class DeviceNotifier(Device):
        name = "Device Notifier"
        def deviceActions(self):
            return []

        def actionNew(self):
            return None
            
        def __init__(self):
            print "INIT: DeviceNotifier"
            self.mainloop=dbus.mainloop.qt.DBusQtMainLoop(set_as_default=True)
            self.systemBus = dbus.SystemBus()
            self._load_drivers()
            self.setup_handlers()

        def setup_handlers(self):
            """Setup handlers for device added 
               and removed events"""
            # Using HAL
            # Taken from:
            # http://stackoverflow.com/questions/469243/how-can-i-listen-for-usb-device-inserted-events-in-linux-in-python
            # TODO: Check if UDisks is a better option
            # TODO: How do we do this on Windows?
            self.hal_mgr_obj = self.systemBus.get_object('org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')
            self.hal_mgr = dbus.Interface(self.hal_mgr_obj, 'org.freedesktop.Hal.Manager')
            self.hal_mgr.connect_to_signal('DeviceAdded', self._device_added)

        def _load_drivers(self):
            self._drivers = []

        def check_mounts(self):
            """Check for devices currently mounted"""
            pass

        def _device_added(self, udi):
            """Handler for the DeviceAdded event"""
            print "Checking device with UDI: ", udi
            device_obj = self.systemBus.get_object('org.freedesktop.Hal', udi)
            device = dbus.Interface(device_obj, 'org.freedesktop.Hal.Device')
            try:
                print "Product: %s"%device.GetProperty('info.product')
                print "Vendor: %s"%device.GetProperty('info.vendor')
            except dbus.DBusException:
                print "Failed to get product and vendor information from device"

            if device.QueryCapability('usb_device'):
                self.check_usb(device)
            if device.QueryCapability('volume'):
                self.check_volume(device)

        def check_usb(self, usb):
            print "Checking USB: ", usb
            print "Device Class: %s"%usb.GetProperty('usb_device.device_class')
            print "Speed: %s"%usb.GetProperty('usb_device.speed_bcd')
            print "Serial: %s"%usb.GetProperty('usb_device.serial')
            print "Product: %s"%usb.GetProperty('usb_device.product')
            print "Vendor: %s"%usb.GetProperty('usb_device.vendor')

        def check_volume(self, volume):
            print "Checking volume: ", volume
            device_file = volume.GetProperty("block.device")
            label = volume.GetProperty("volume.label")
            fstype = volume.GetProperty("volume.fstype")
            mounted = volume.GetProperty("volume.is_mounted")
            mount_point = volume.GetProperty("volume.mount_point")
            try:
                size = volume.GetProperty("volume.size")
            except:
                size = 0

            print "New storage device detectec:"
            print "  device_file: %s" % device_file
            print "  label: %s" % label
            print "  fstype: %s" % fstype
            if mounted:
                print "  mount_point: %s" % mount_point
            else:
                print "  not mounted"
            print "  size: %s (%.2fGB)" % (size, float(size) / 1024**3)



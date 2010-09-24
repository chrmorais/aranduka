from pluginmgr import Device

import sys
import dbus
import dbus.mainloop.qt
from PyQt4 import QtCore


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
        self.sessionBus = dbus.SessionBus()

        self.sessionBus.add_signal_receiver(signal_name="MountAdded",
                                    dbus_interface="org.gtk.Private.RemoteVolumeMonitor",
                                    path="/org/gtk/Private/RemoteVolumeMonitor",
                                    bus_name=None,
                                    handler_function=self.mountDetected)

    def mountDetected(self, sender, mount_id, data):
        print "New drive mounted at %s" % data[4][7:]
        print mount_id
        print data



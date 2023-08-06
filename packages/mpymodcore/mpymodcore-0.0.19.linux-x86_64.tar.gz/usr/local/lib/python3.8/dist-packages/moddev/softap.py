"""
    (c)2020 K. Goger (k.r.goger@gmail.com)
    legal: https://github.com/kr-g/mpymodcore/blob/master/LICENSE
"""

import uos
import network

import machine
import binascii

from modcore import modc, Module, LifeCycle

SOFTAP_CFG = "softap.cfg"
ID_SPEC = "$id$"


class SoftAP(Module):
    def init(self):
        self.last_status = False

    def update(self):
        try:
            self.last_status = self.ap.active()
        except:
            self.last_status = False

    def start(self):
        self.softap_start()
        # self.update()

    def loop(self, config=None, event=None):
        if self.current_level() != LifeCycle.RUNNING:
            return
        status = self.ap.active()
        if status != self.last_status:
            self.update()
            self.fire_event("softap", status)

    def stop(self):
        self.softap_stop()
        # self.update()

    # deprecated

    def softap_config(self, ssid, passwd):
        """set softap ssid and password for automatic connection during startup"""
        softap_cfg = "\n".join([ssid, passwd])
        if passwd == None or len(passwd) < 8:
            raise Exception("password too short")
        try:
            with open(SOFTAP_CFG, "wb") as f:
                f.write(softap_cfg)
        except Exception as ex:
            self.excep(ex, "config")

    def softap_remove(self):
        """remove softap info and disable automatic connection during startup"""
        self.softap_stop()
        uos.remove(SOFTAP_CFG)

    def softap_start(self, active=True):
        """start softap if configured before, otherwise do nothing"""
        try:
            self.ap = network.WLAN(network.AP_IF)
            self.ap.active(False)
        except Exception as ex:
            self.excep(ex)

        try:
            with open(SOFTAP_CFG) as f:
                content = f.read()
        except Exception as ex:
            # not configured fo autostart
            return

        try:
            lines = map(lambda x: x.strip(), content.split("\n"))
            lines = filter(lambda x: len(x) > 0, lines)
            credits = list(filter(lambda x: x.find("#") != 0, lines))

            if active:
                self.ap.active(active)

                ssid = credits[0].strip()
                passw = credits[1].strip()

                pos = ssid.find(ID_SPEC)
                if pos >= 0:
                    uid = binascii.hexlify(machine.unique_id()).decode()
                    ssid = ssid.replace(ID_SPEC, uid)
                    self.info("unique ssid", ssid)

                self.ap.config(essid=ssid)
                self.ap.config(authmode=3, password=passw)
                self.info("network info", self.ap.ifconfig())

        except Exception as ex:
            self.excep(ex, "start")

    def softap_stop(self):
        """disabled softap, no reconfiguration of prior configuration"""
        self.softap_start(active=False)

    def ifconfig(self):
        return self.ap.ifconfig()

    def active(self):
        return self.ap.active()

    def mac(self):
        return self.ap.config("mac")


soft_ap = SoftAP("soft_ap")
modc.add(soft_ap)

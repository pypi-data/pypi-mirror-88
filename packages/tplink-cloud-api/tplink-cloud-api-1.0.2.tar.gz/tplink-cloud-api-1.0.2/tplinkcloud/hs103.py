from .device_type import TPLinkDeviceType
from .device import TPLinkDevice

class HS103Action:
    
    def __init__(self, action):
        self.action = action.get('type')

class HS103SysInfo:

    def __init__(self, sys_info):      
        self.sw_ver = sys_info.get('sw_ver')
        self.hw_ver = sys_info.get('hw_ver')
        self.model = sys_info.get('model')
        self.device_id = sys_info.get('deviceId')
        self.oem_id = sys_info.get('oemId')
        self.hw_id = sys_info.get('hwId')
        self.rssi = sys_info.get('rssi')
        self.longitude_i = sys_info.get('longitude_i')
        self.latitude_i = sys_info.get('latitude_i')
        self.alias = sys_info.get('alias')
        self.status = sys_info.get('status')
        self.mic_type = sys_info.get('mic_type')
        self.feature = sys_info.get('feature')
        self.mac = sys_info.get('mac')
        self.updating = sys_info.get('updating')
        self.led_off = sys_info.get('led_off')
        self.relay_state = sys_info.get('relay_state')
        self.on_time = sys_info.get('on_time')
        self.active_mode = sys_info.get('active_mode')
        self.icon_hash = sys_info.get('icon_hash')
        self.dev_name = sys_info.get('dev_name')
        self.next_action = HS103Action(sys_info.get('next_action'))
        self.err_code = sys_info.get('err_code')  

class HS103(TPLinkDevice):

    def __init__(self, client, device_id, device_info):
        super().__init__(client, device_id, device_info)
        self.model_type = TPLinkDeviceType.HS103

    def get_sys_info(self):
        sys_info = self._get_sys_info()
        return HS103SysInfo(sys_info)

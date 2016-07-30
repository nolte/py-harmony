"""Client class for connecting to the Logitech Harmony."""

import json
import logging
import time

import sleekxmpp
from sleekxmpp.xmlstream import ET


LOGGER = logging.getLogger(__name__)

def buildAction_cmd(action, command):
    LOGGER.info("build command component")
    action_cmd = ET.Element('oa')
    action_cmd.attrib['xmlns'] = 'connect.logitech.com'
    action_cmd.attrib['mime'] = (
        'vnd.logitech.harmony/vnd.logitech.harmony.engine?'+action)
    
    if command:
       LOGGER.info("Original: %s",command)    
       # At this point our valid json won't work - we need to break it so it looks like:
       # {"type"::"IRCommand","deviceId"::"deviceId","command"::"command"}
       # note double colons 
       encodedAction = command.replace(':', '::').replace(' ', "")
       LOGGER.info("Encoded: %s",encodedAction)
       action_cmd.text =  "action="+encodedAction+":status=press"
          
    return action_cmd          


class HarmonyClient(sleekxmpp.ClientXMPP):
    """An XMPP client for connecting to the Logitech Harmony."""

    def __init__(self):
        user =  'guest@x.com/gatorade'
        password = 'guest'
        plugin_config = {
            # Enables PLAIN authentication which is off by default.
            'feature_mechanisms': {'unencrypted_plain': True},
        }
        LOGGER.info("init component")
        super(HarmonyClient, self).__init__(
            user, password, plugin_config=plugin_config)

    def sendCommand(self,command):
        """Send a command to the harmony Hub.
        """
        LOGGER.debug("send command %s",command)
        iq_cmd = self.Iq()
        iq_cmd['type'] = 'get'
        action_cmd = buildAction_cmd("holdAction",command)
        iq_cmd.set_payload(action_cmd)
        
        iq_cmd.send(block=False)
        return True       

    def get_config(self):
        """Retrieves the Harmony device configuration.

        Returns:
          A nested dictionary containing activities, devices, etc.
        """
        LOGGER.info("get the config")
        iq_cmd = self.Iq()
        iq_cmd['type'] = 'get'
        action_cmd = buildAction_cmd("config")
        iq_cmd.set_payload(action_cmd)
        result = iq_cmd.send(block=True)
        payload = result.get_payload()
        assert len(payload) == 1
        action_cmd = payload[0]
        assert action_cmd.attrib['errorcode'] == '200'
        device_list = action_cmd.text
        return json.loads(device_list)


def create_and_connect_client(ip_address, port):
    """Creates a Harmony client and initializes session.

    Args:
      ip_address: IP Address of the Harmony device.
      port: Port that the Harmony device is listening on.

    Returns:
      An instance of HarmonyClient that is connected.
    """
    LOGGER.debug("start connect to hub %s:%s",ip_address, port)
    client = HarmonyClient()
    
    client.connect(address=(ip_address, port),
                   use_tls=False, use_ssl=False)
    client.process(block=False)

    while not client.sessionstarted:
        time.sleep(0.1)

    LOGGER.info("connected to harmony hub %s:%s",ip_address, port)
    return client

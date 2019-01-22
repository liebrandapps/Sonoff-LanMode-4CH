# Sonoff-LanMode-4CH
Control your 4CH Sonoff Device with stock firmware (e.g. 2.7.1) without Cloud in Lan Mode

https://www.liebrand.io/operate-4ch-sonoff-device-w-o-cloud/

This sample code allows to control a Sonoff WLAN 4 CH Switch w/o cloud. It has been tested with firmware 2.7.1. Older firmware
probably works as well. If you can connect to port 8081 of your device (e.g. telnet), it looks like LAN Mode is working.

Please make sure that always only 1 (one) client is connected to the device. If a connection is established a second connection 
is refused.

The code can be run standalone and switches outlet 0 of the 4CH on and off. Stdout out shows what is being sent and received. 
The software runs the receiver in a separate thread. Status changes (e.g. by hardware button press) result in a message. 
After action 'userOnline', two JSONs are sent subsequently. The second reveals the outlet status.

You may need to install the websocket-client package to run.

The code should also work with single switch devices. Yet untested as I don't have such a device. Just omit the outlet parameter
of the updateMessage() method.

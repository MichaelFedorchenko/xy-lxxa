import time
import xy_lxxa as UPSC
"""
DEMO DEMO DEMO DEMO DEMO DEMO DEMO DEMO DEMO DEMO DEMO
"""
ups = UPSC.XYCTRL('/dev/tty.usbserial-0001', 9600)

print('##### DEMO 1 - READ MEASURES')
try:
    data = ups.readMeasure()
    if data == 'NO_DATA':
        print('Can not read measures from controller...')
    else:
        V, P, T, S = data
        print(f'Battery: {V}')
        print(f'Charge: {P}')
        print(f'Time: {T}')
        state = 'ON' if S == 'CL' else 'OFF'
        print(f'State: {state}')
except Exception as e:
    print(e)


time.sleep(3)


print('\n\n##### DEMO 2 - READ SETTINGS')
try:
    data = ups.readSettings()
    if data == 'NO_DATA':
        print('Can not read settings from controller...')
    else:
        LV, HV, T = data
        print(f'Low Voltage: {LV}')
        print(f'High Voltage: {HV}')
        print(f'Time: {T}\n')
except Exception as e:
    print(e)


time.sleep(3)


print('\n\n##### DEMO 3 - SET VOLTAGE')
try:
    if ups.setVoltage(12.1, 12.6) == 'OK':
        print('Set Voltage OK')
except Exception as e:
    print(e)


time.sleep(3)


print('\n\n##### DEMO 4 - TOGGLE RELAY')
try:
    if ups.control(1) == 'ON':
        print('Relay is ON')
    else:
        print('Relay is OFF')
    time.sleep(.9)
    if ups.control(0) == 'ON':
        print('Relay is ON')
    else:
        print('Relay is OFF')
except Exception as e:
    print(e)

time.sleep(3)


print('\n\n##### DEMO 5 - SET TIME')
try:
    if ups.setTime(0, 10) == 'OK':
        print('Set timer OK (10 minutes)')
    else:
        print('Can not set up timer')
except Exception as e:
    print(e)


time.sleep(3)


print('\n\n##### DEMO 6 - DISCONNECT')
try:
    if ups.disconnect() == 'DISCONNECTED':
        print('Disconnected successfully')
    else:
        print('Can not disconnect')
except Exception as e:
    print(e)


time.sleep(3)

print('\n\n##### DEMO 7 - CONNECT AND SUBSCRIBE ON STREAM')
print('##### PRESS CTRL+C TO STOP STREAM AND DISCONNECT FROM PORT')
ups = UPSC.XYCTRL(port='/dev/tty.usbserial-0001', baudrate=9600)
streamWorks = False
try:
    if ups.startStream() == 'STREAM_STARTED':
        print('Stream started successfully')
        streamWorks = True
except Exception as e:
    print(e)
# Read data from stream
count = 1
try:
    while streamWorks:
        data = ups.readFromStream()
        if data == 'NO_DATA':
            print('Can not read measures from stream')
        else:
            V, P, T, S = data
            counter = '{:0>5.0f}'.format(count)
            print(f'\n----------{counter}----------')
            print(f'Battery: {V}')
            print(f'Charge: {P}')
            print(f'Time: {T}')
            state = 'ON' if S == 'CL' else 'OFF'
            print(f'State: {state}')
        count += 1
        time.sleep(3)
except Exception as e:
    print(e)
    streamWorks = False

except KeyboardInterrupt:
    pass
finally:
    try:
        if ups.stopStream() == 'STREAM_STOPPED':
            print('Stream stop OK')
        else:
            print('Can not stop stream')
    except Exception as e:
        print(e)
    ups.disconnect()

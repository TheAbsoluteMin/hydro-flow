import time
import board
import pwmio
import digitalio
import analogio
import adafruit_dht
import math

#define and turn off actuators at start
pump = pwmio.PWMOut(board.GP11, frequency=5000, duty_cycle=0)
fan = pwmio.PWMOut(board.GP13, frequency=25000, duty_cycle=0) 

#define switch
system_switch = digitalio.DigitalInOut(board.GP12)
system_switch.direction = digitalio.Direction.INPUT
system_switch.pull = digitalio.Pull.UP 

#define sensors
dht_sensor = adafruit_dht.DHT22(board.GP14)
ice_probe = analogio.AnalogIn(board.GP26)

#scale temperature readings for accuracy
def scale_pwm(percentage):
    clamped_percentage = max(0.0, min(100.0, percentage))
    return int((clamped_percentage / 100.0) * 65535)

#measure ice temperature
def read_ice_temperature():
    raw_adc = ice_probe.value
    
    if raw_adc <= 100 or raw_adc >= 65400: 
        return 25.0 #temperature boundaries
    
    try:
        resistance = 10000 / ((65535 / raw_adc) - 1)
        steinhart = resistance / 10000
        steinhart = math.log(steinhart)
        steinhart /= 3950
        steinhart += 1.0 / (25 + 273.15)
        steinhart = 1.0 / steinhart
        
        return steinhart - 273.15
    except (ZeroDivisionError, ValueError):
        return 4.0 #handle math errors

#switch states
system_active = False       
last_switch_state = True    
last_debounce_time = 0.0    
DEBOUNCE_DELAY = 0.05       

#DHT22 default states to prevent code glitches when AC unit switches on/off
room_temp = 24
room_humidity = 50
last_dht_read_time = 0
DHT_READ_INTERVAL = 2

#loop
while True:
    current_time = time.monotonic() #read current time
    current_switch_reading = system_switch.value  
    
    if current_switch_reading != last_switch_state:
        if (current_time - last_debounce_time) > DEBOUNCE_DELAY:
            if current_switch_reading == False:
                system_active = not system_active
            last_debounce_time = current_time
    last_switch_state = current_switch_reading  

    if not system_active:
        fan.duty_cycle = 0 #turn actuators off
        pump.duty_cycle = 0
        time.sleep(0.01)  
        continue

    
    ice_temp = read_ice_temperature()

    if (current_time - last_dht_read_time) >= DHT_READ_INTERVAL:
        try:
            sampled_temp = dht_sensor.temperature
            sampled_hum = dht_sensor.humidity
            
            if sampled_temp is not None: room_temp = sampled_temp
            if sampled_hum is not None: room_humidity = sampled_hum
            
            last_dht_read_time = current_time
        except RuntimeError:
            pass

    pump_output = 0
    fan_output = 0

    #staged chilling modes allow for constant chill feel despite melting ice over time

    #stage 1: slow chill
    if ice_temp < 4:
        pump_output = 30
        fan_output = 45

        #excessive heat case: increase fan speed
        if room_temp > 28:
            fan_output = 55
    
    #stage 2: moderate chill
    elif 4 <= ice_temp < 12:
        pump_output = 65
        fan_output = 70
    
    #stage 3: max chill
    else:
        pump_output = 100
        fan_output = 100
    
    #high humidity case: lower fan speed to allow more time for air to reduce moisture through copper tubes
    if room_humidity > 70:
        fan_output*=0.85

    fan.duty_cycle = scale_pwm(fan_output)
    pump.duty_cycle = scale_pwm(pump_output)

    time.sleep(0.05)

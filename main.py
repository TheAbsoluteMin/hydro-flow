import time
import board
import pwmio
import digitalio
import analogio
import adafruit_dht
import math

pump = pwmio.PWMOut(board.GP11, frequency=5000, duty_cycle=0)
fan = pwmio.PWMOut(board.GP13, frequency=25000, duty_cycle=0) 

system_switch = digitalio.DigitalInOut(board.GP12)
system_switch.direction = digitalio.Direction.INPUT
system_switch.pull = digitalio.Pull.UP 

dht_sensor = adafruit_dht.DHT22(board.GP14)

ice_probe = analogio.AnalogIn(board.GP26)

def scale_pwm(percentage):
    clamped_percentage = max(0.0, min(100.0, percentage))
    return int((clamped_percentage / 100.0) * 65535)

def read_ice_temperature():
    raw_adc = ice_probe.value
    
    if raw_adc <= 100 or raw_adc >= 65400: 
        return 25.0 
    
    try:
        resistance = 10000 / ((65535 / raw_adc) - 1)
        
        steinhart = resistance / 10000
        steinhart = math.log(steinhart)
        steinhart /= 3950
        steinhart += 1.0 / (25 + 273.15)
        steinhart = 1.0 / steinhart
        
        return steinhart - 273.15
    except (ZeroDivisionError, ValueError):
        return 4.0

system_active = False       
last_switch_state = True    
last_debounce_time = 0.0    
DEBOUNCE_DELAY = 0.05       

room_temp = 24
room_humidity = 50
last_dht_read_time = 0
DHT_READ_INTERVAL = 2


while True:
    current_time = time.monotonic()
    current_switch_reading = system_switch.value  
    
    if current_switch_reading != last_switch_state:
        if (current_time - last_debounce_time) > DEBOUNCE_DELAY:
            if current_switch_reading == False:
                system_active = not system_active
            last_debounce_time = current_time
    last_switch_state = current_switch_reading  

    if not system_active:
        fan.duty_cycle = 0
        pump.duty_cycle = 0
        time.sleep(0.01)  
        continue

    
    ice_temp = read_ice_temperature()

    if current_time - last_dht_read_time >= DHT_READ_INTERVAL:
        try:
            sampled_temp = dht_sensor.temperature
            sampled_hum = dht_sensor.humidity
            
            if sampled_temp is not None: room_temp = sampled_temp
            if sampled_hum is not None: room_humidity = sampled_hum
            
            last_dht_read_time = current_time
        except RuntimeError:
            pass

    baseline_pump_speed = 50.0
    baseline_fan_speed = 60.0

    fan.duty_cycle = scale_pwm(baseline_fan_speed)
    pump.duty_cycle = scale_pwm(baseline_pump_speed)

    time.sleep(0.05)

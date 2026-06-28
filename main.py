import time
import board
import pwmio
import digitalio
import analogio
import adafruit_dht
import math
import neopixel
import busio
import terminalio
import displayio
import fourwire
from adafruit_gc9a01 import GC9A01
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect

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

#define LEDs
pixels = neopixel.NeoPixel(board.GP15, 30, brightness=0.20, auto_write=False)
pixels.fill((0,0,0))
pixels.show()

#define GC9A01 LCD Display
displayio.release_displays()
spi = busio.SPI(clock=board.GP16, MOSI=board.GP17)
tft_res = board.GP18
tft_dc = board.GP19
tft_cs = board.GP20
tft_bl = board.GP21
display_bus = fourwire.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_res)
display = GC9A01(display_bus, width=240, height=240, rotation=0, backlight_pin=tft_bl)

#define ui features for GC9A01 LCD Display
ul_group = displayio.Group()
display.root_group = ui_group

header_lbl = label.Label(terminalio.FONT, text="HydroFlow", color=0x00FF00)
header_lbl.x, header_lbl.y = 80, 40
ui_group.append(header_lbl)

room_lbl = label.Label(terminalio.FONT, text="Room: --.-C", color=0xFFFFFF, scale=2)
room_lbl.x, room_lbl.y = 50, 100
ui_group.append(room_lbl)

humidity_lbl = label.Label(terminalio.FONT, text="Humidity: --%", color=0x00FFFF, scale=1)
humidity_lbl.x, humidity_lbl.y = 85, 135
ui_group.append(humidity_lbl)

bar_frame = Rect(50, 170, 140, 12, outline=0x555555, stroke=1)
ui_group.append(bar_frame)

ice_bar = Rect(51, 171, 138, 10, fill=0x0000FF)
ui_group.append(ice_bar)

ice_lbl = label.Label(terminalio.FONT, text="Ice: --.-C", color=0xAAAAAA)
ice_lbl.x, ice_lbl.y = 75, 200
ui_group.append(ice_lbl)

#update LEDs
def update_led_ridge(color_rgb):
    pixels[0:20]=[color_rgb]*20
    pixels[20:30]=[(0,0,0)]*10
    pixels.show()

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
        #turn actuators off
        fan.duty_cycle = 0
        pump.duty_cycle = 0

        update_led_ridge((0,0,0))

        #static off screen
        room_lbl.text = "System Off"
        room_lbl.x = 77
        humidity_lbl.text = ""
        ice_lbl.text = "Press to start"
        ice_lbl.x = 75
        ice_bar.width = 0

        time.sleep(0.05)  
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

    room_lbl.x, humidity_lbl.x, ice_lbl.x = 50, 85, 75

    #staged chilling modes allow for constant chill feel despite melting ice over time

    #stage 1: slow chill
    if ice_temp < 4:
        pump_output = 30
        fan_output = 45

        #excessive heat case: increase fan speed
        if room_temp > 28:
            fan_output = 55
        led_color = (0, 128, 255)
    
    #stage 2: moderate chill
    elif 4 <= ice_temp < 12:
        pump_output = 65
        fan_output = 70
        led_color = (0, 255, 128)
    
    #stage 3: max chill
    else:
        pump_output = 100
        fan_output = 100
        led_color = (255, 60, 0)
    
    #high humidity case: lower fan speed to allow more time for air to reduce moisture through copper tubes
    if room_humidity > 70:
        fan_output*=0.85

    fan.duty_cycle = scale_pwm(fan_output)
    pump.duty_cycle = scale_pwm(pump_output)
    update_led_ridge(led_color)

    #update LCD screen metrics
    room_lbl.text = "Room: {:.1f}C".format(room_temp)
    humidity_lbl.text = "Humidity: {:.0f}%".format(room_humidity)
    ice_lbl.text = "Ice: {:.1f}C".format(ice_temp)

    #ice pack bar
    remaining_ice_ratio = (25-ice_temp)/25
    ice_bar.width = int(138*max(0,min(1,remaining_ice_ratio)))

    time.sleep(0.05)

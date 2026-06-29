# HydroFlow: Closed-loop, radiator-style revisioned desktop AC

HydroFlow is an automated, condensation-based personal cooling system designed to replace standard swamp coolers that cool an area by evaporating water. 

Swamp coolers add uncomfortable amounts of humidity and sticky moisture into the air. HydroFlow seeks to solve this problem by circulating freezing water through a tightly packed, flattened copper serpentine loop sitting behind a fan. This effectively cools down the air temperature while stripping away the humidity and moisture from the environment.

<img src="https://cdn.hackclub.com/019f0fd8-e2bb-7ff8-b522-9a8814e6d1cc/image.png" alt="image"/>

---

## Key Features
* **No Humidity Cooling Matrix**: Uses a closed thermal conduction loop to lower temperature and condense water droplets out of the air.
* **Flattened Oval Serpentine Copper Coils**: Allows for high-efficiency heat draining.
* **Automated Smart Cooling**: Features a three stage adaptive algorithm driven by temperature readings.
* **LED Feedback**: Integrates a 20 NeoPixel LEDs that indicate the current cooling stage.
* **Circular LCD Display**: Features a real-time dashboard displaying system status, temperature metrics, and ice depletion.

---

## Automated Smart Firmware Logic

The firmware uses a smart state-machine that adjusts pump flow fan speeds as the ice temperature melts and increases in temperature over time during use.

The fan also takes into account these two extreme cases:

* **Extreme Room Heat**: If Stage 1 is active but room temperature exceeds 28°C, the fan automatically increases fan speed from 45% to 55% to force immediate cooling.
* **High Humidity**: If room humidity climbs past 70%, the fan's speed decreases by 15%. This increases air flow time over the freezing copper tubes in order to maximize the moisture condensation rate, which lowers the cooling air temperature further.

---

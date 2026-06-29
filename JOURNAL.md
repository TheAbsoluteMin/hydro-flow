---
title: "HydroFlow"
author: "TheAbsoluteMin"
description: "Closed-loop, radiator-style revisioned desktop AC."
created_at: "2026-06-17"
---

# HydroFlow Development Log

## Log 1: June 17, 2026 - Schematics and PCB - 7 hours
Timelapse <a href="https://lapse.hackclub.com/timelapse/Oom849_IEaSS">link</a>.

Welcome! The story of HydroFlow begins three years ago... ever since the central AC system of my house broke down. For three summers, I had to lie in bed in the smothering heat. For three summers, I had to rely on cheap fans with ice. For three summers, I had to think of some way to stay cool without spending too much money nor electricity... That all changed this summer when I figured out that I could reverse engineer those cheap fans. Knowing the potential funding by the Hack Club organization, I decided it was time HydroFlow was born.

Specifically, today, I designed the schematics and custom PCB board for my desktop cooler project. Soon, I would make a compact smart fan system that saves ice and electricity by efficiently dry cooling by blowing on copper tubes filled with pumped ice water! This would remove the swampy humid chill of ice water fans while replacing it with the cool, dry feel of an air conditioning unit!

<img width="1836" height="694" alt="image" src="https://github.com/user-attachments/assets/3e14bf40-7e3c-4c5c-974f-e664fa262a31" />
<img width="1479" height="824" alt="image" src="https://github.com/user-attachments/assets/ad89a049-f560-404f-9eb4-6b04babd3904" />

A key feature of my PCB included the use of different track widths for the power lines and data lines. Since my project included an MT3608 DC-DC Step-Up Boost Module to boost my 5 volt input power to 12 volts for the 12 volt rated fan, I had to maintain a thick track width of about 1mm. On the other hand, the data lines remained at a minimal 0.25mm width.

### Struggles:
My biggest roadblock was managing the physical space and the power constraints on a small, horizontal board without causing a system failure. I was scared of experiencing another system brownout like my past stepper motor project, especially while trying to fit a bulky, huge screen backing plate with an oversized voltage booster module and Raspberry Pi Pico 2. On top of that, KiCad kept throwing me critical design errors!

### Future work:
With some simple math, I made sure that my 5 volt power source had enough headroom, and I finally fit everything in the PCB! I look forward to adding mounting screw holes and exporting my PCB so that I can begin to work on the CAD for the case design!

---

## Log 2: June 18, 2026 - CAD Design - 4 hours
Timelapse <a href="https://lapse.hackclub.com/timelapse/BJVgF5JaslK2">link</a>.

I had to make a minor update to my PCB board regarding some GND routing. I intentionally split GND into GND (common) and GND_POWER in order to separate the GND noise from the fan from the rest of the components of HydroFlow. With this, I only allowed a single connection at the USB GND pad where all the noise from the fan's GND line could dump and connect to the common GND. I also began to work on the CAD design for HydroFlow's case. What started as a simple box frame quickly became a test of patience and critical thinking! I had to triple check all the measurements for all my parts again and then work on the details.

<img width="932" height="538" alt="image" src="https://github.com/user-attachments/assets/f093a120-c56f-4e22-8c8c-67f929561b5b" />

### Struggles:
The most difficult part was designing the snap fits for my copper tubing in the back! I really want to loop each row of tubing in the back as close together as possible, but I am not sure how strong the copper tubing is... I will design with theoretical numbers for now, and when I get the actual parts, I know that I will have to go through all the CAD design measurements again!!! Oh, the many hours of repetitive tasks! Yet, they teach me so much.

<img width="708" height="713" alt="image" src="https://github.com/user-attachments/assets/4a84b556-72be-4f0a-bb70-9135a6a69008" />

### Future work:
Next time, I will continue to design the case and its interior, including holes for all the wiring and components for HydroFlow.

---

## Log 3: June 19, 2026 - CAD Design Completion - 2.1 hours
Timelapse <a href="https://lapse.hackclub.com/timelapse/JToWWzL-IyvG">link</a>.

With two more hours, I integrated the PCB board into my design for scaling, and I carved out some more holes for the wiring of the sensors throughout HydroFlow's case. Finally, after so much time struggling with learning how to use Autodesk Fusion, the model was completed! I even figured out how to add color to my 3D design!

<img width="627" height="764" alt="image" src="https://github.com/user-attachments/assets/76c5c52d-5d40-4cd9-af89-bca0d8e5b0bf" />
<img width="602" height="878" alt="image" src="https://github.com/user-attachments/assets/5e59c8ef-d33b-4f32-a1b7-277889fcaf6a" />

### Struggles:
It was difficult trying to control exterior components, like the PCB step file, as I had to configure it so that I could actually edit it and move it to the correct location in the model. Furthermore, ensuring that all the parts were in the right place with accurate and precise dimensions was a nightmare!

<img width="726" height="721" alt="image" src="https://github.com/user-attachments/assets/404420a5-b2a5-44d1-8003-f902ac5fd126" />

### Future work:
After this milestone, I will begin to work on the code that brings my smart custom AC fan to life!

---

## Log 4: June 28, 2026 - Code - 2.5 hours
Hours logged with Hackatime

Today, I decided to work on the code for HydroFlow, and I learned a lot through coding references on how to bring my hardware modules to life through CircuitPython from defining pins of the fan and pump module to creating functions for the DHT22 and NTC temperature sensors so they could measure the temperature. In the code loop, HydroFlow uses the data from the temperature sensors to automatically adapt to the environment temperature and humidity and the ice pack and water temperature. Specifically, in the beginning the pump and fan speeds are slow, but as the ice melts and gets hotter, the pump pushes water faster and the fan speed increases in order to maintain the same level of chill as that of when the ice was fresh. This smart loop serves to improve on the design of static fans by balancing the coolness of the air output and the ice life.

<img width="1848" height="810" alt="image" src="https://github.com/user-attachments/assets/82a82b6c-190a-4fbc-903e-087a07569c47" />

### Struggles:
I spent a lot of time learning hardware specific code that I was unfamiliar with. For example, I did not know that the GC9A01 LCD display screen required many setup and definition functions in order to get it to display simple temperature metrics! It was also not easy to use the Steinhart–Hart equation to accurately read the NTC temperature sensor!

<img width="587" height="388" alt="image" src="https://github.com/user-attachments/assets/176b21e6-0d22-4889-9262-4359293519e8" />

### Future work:
As I have finished the design for HydroFlow, I look forward to actually ordering the parts and building the entire project!

---

---
title: "HydroFlow"
author: "TheAbsoluteMin"
description: "Desktop AC Revisioned"
created_at: "2026-06-17"
---

# HydroFlow Development Log

## Log 1: June 17, 2026 - Schematics and PCB - 6.5 hours
Timelapse <a href="https://lapse.hackclub.com/timelapse/Oom849_IEaSS">link</a>.

Welcome! The story of HydroFlow begins three years ago... ever since the central AC system of my house broke down. For three summers, I had to lie in bed in the smothering heat. For three summers, I had to rely on cheap fans with ice. For three summers, I had to think of some way to stay cool without spending too much money nor electricity... That all changed this summer when I figured out that I could reverse engineer those cheap fans. Knowing the potential funding by the Hack Club organization, I decided it was time HydroFlow was born.

Specifically, today, I designed the schematics and custom PCB board for my desktop cooler project. Soon, I would make a compact smart fan system that saves ice and electricity by efficiently dry cooling by blowing on copper tubes filled with pumped ice water! This would remove the swampy humid chill of ice water fans while replacing it with the cool, dry feel of an air conditioning unit!

<img width="1836" height="694" alt="image" src="https://github.com/user-attachments/assets/3e14bf40-7e3c-4c5c-974f-e664fa262a31" />
<img width="1479" height="824" alt="image" src="https://github.com/user-attachments/assets/ad89a049-f560-404f-9eb4-6b04babd3904" />

### Struggles:
My biggest roadblock was managing the physical space and the power constraints on a small, horizontal board without causing a system failure. I was scared of experiencing another system brownout like my past stepper motor project, especially while trying to fit a bulky, huge screen backing plate with an oversized voltage booster module and Raspberry Pi Pico 2. On top of that, KiCad kept throwing me critical design errors!

### Future work:
With some simple math, I made sure that my 5 volt power source had enough headroom, and I finally fit everything in the PCB! I look forward to adding mounting screw holes and exporting my PCB so that I can begin to work on the CAD for the case design!

---

## Log 2: June 18, 2026 - CAD Design - 3.5 hours
Timelapse <a href="https://lapse.hackclub.com/timelapse/BJVgF5JaslK2">link</a>.

After making a minor update to my PCB board regarding some GND routing, I began to work on the CAD design for HydroFlow's case. What started as a simple box frame quickly became a test of patience and critical thinking! I had to triple check all the measurements for all my parts again and then work on the details.

<img width="932" height="538" alt="image" src="https://github.com/user-attachments/assets/f093a120-c56f-4e22-8c8c-67f929561b5b" />

### Struggles:
The most difficult part was designing the snap fits for my copper tubing in the back! I really want to loop each row of tubing in the back as close together as possible, but I am not sure how strong the copper tubing is... I will design with theoretical numbers for now, and when I get the actual parts, I know that I will have to go through all the CAD design measurements again!!! Oh, the many hours of repetitive tasks! Yet, they teach me so much.

<img width="708" height="713" alt="image" src="https://github.com/user-attachments/assets/4a84b556-72be-4f0a-bb70-9135a6a69008" />

### Future work:
Next time, I will continue to design the case and its interior, including holes for all the wiring and components for HydroFlow.

---

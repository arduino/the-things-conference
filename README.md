# The Things Conference Workshop
Think machine vision and machine learning is difficult to do on microcontrollers? Find out how to leverage cutting edge technology for developing LoRa powered solutions which run machine vision algorithms efficiently.
This repository hosts all the content and demo code to recreate the demos presented in Arduino's Things Conference Workshop hosted by Sebastian Romero ([@sebromero](https://github.com/sebromero)).

## What You Will Learn
- How to use the Arduino / OpenMV infrastructure to connect to a LoRa network
- How to do simple object detection using OpenMV
- How to run a custom machine learning model for machine vision applications

## Required Hardware and Software
To try out all the examples you need to download some additional software and register an account with The Things Network and Edge Impulse.

- The **Arduino IDE** can be downloaded from [this website](https://www.arduino.cc/en/software)
- The **OpenMV IDE** can be downloaded from [this website](https://openmv.io/pages/download)

- If you want to test the LoRa connectivity of the Portenta Vision Shield LoRa, you can register an account with **The Things Network** [here](https://account.thethingsnetwork.org/register).
- To create your own custom machine learning models as seen in the demos, you need to register an **Edge Impulse** account [here](https://studio.edgeimpulse.com/).

## Preparing the Arduino IDE for Portenta
Open the Arduino IDE and then open the board manager from the Tools menu. Search for "portenta". Find the Arduino mbed-enabled Boards library and click on "Install" to install the latest version of the mbed core (1.3.1 at the time of writing this guide). This is the software that allows you to access the Portenta's features. Choose the first one in the list, not the one which says "DEPRECATED". Once the installation completes, the Arduino IDE will be ready for your Portenta board.

More information on getting started with Portenta can be found [here](https://www.arduino.cc/pro/tutorials/portenta-h7/por-ard-gs).

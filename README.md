# RISurfaces

## Description
The project aims to develop software that allows the control of a measurement system to test the possibility of usage RIS'es (reconfigurable intelligent surfaces) for use in 6th generation radio systems.

## Code
The project consists of modules that are direct equivalents of actual measuring equipment. So we have a module responsible for controlling the spectrum analyzer, signal generator, antenna array, rotating head on which the array is mounted. Also there are modules responsible for individual measurement scenarios.

## Communictaion 
Communication between modules is carried out using a computer network. The central point is the router. The antenna array can be controlled via USB interface, or Bluetooth Low Energy.

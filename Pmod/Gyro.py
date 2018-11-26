# -*- coding: utf-8 -*-
# Copyright (c) 2017 RS Components Ltd
# SPDX-License-Identifier: MIT License

"""
Interface for PmodGyro.

.. note::
"""

import RPi.GPIO as gpio
from time import sleep
import spidev

CAP = 'SPI'
PHY = '2x6'
READ = 0x80
CTRL_REG1 = 0x20
CTRL_REG2 = 0x21
CTRL_REG3 = 0x22
CTRL_REG4 = 0x23
CTRL_REG5 = 0x24
REGISTRE_MSB_X = 0x29 
REGISTRE_LSB_X = 0x28 
REGISTRE_MSB_Y = 0x2B 
REGISTRE_LSB_Y = 0x2A 
REGISTRE_MSB_Z = 0x2D
REGISTRE_LSB_Z = 0x2C 

WHO_AM_I = 0x0F
INT1_TSH_XH = 0x32
INT1_CFG = 0x30
OUT_X_L = 0x28
OUT_X_H	= 0x29
OUT_Y_L	= 0x2A
OUT_Y_H	= 0x2B
OUT_Z_L	= 0x2C
OUT_Z_H	= 0x2D

class PmodGyro:

    def __init__(self, DSPMod12):
        self.port = DSPMod12
        
        self.cs = self.port.pin1
        self.mosi = self.port.pin2
        self.miso = self.port.pin3
        self.sclk = self.port.pin4
        self.int1 = self.port.pin7
        self.int2 = self.port.pin8
        gpio.setmode(gpio.BCM)
        gpio.setup(self.int1, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(self.int2, gpio.IN, pull_up_down=gpio.PUD_UP)

        self.spi = spidev.SpiDev()
        self.__startSPI()

        while True: 
           if (gpio.input(self.int2) == True): # Physically read the pin now
                    print('3.3')
                    break;
           else:
                    print('0')
           sleep(1);           # Sleep for a full second before restarting our loop


    def __startSPI(self):
        if self.cs == 7: #CE1
            self.serial = self.spi.open(1,0)
        elif self.cs == 8: #CE0
            self.serial = self.spi.open(0,0)
        else:
            #throw exception
            return    
        self.speed_hz = 2000000
        self.spi.max_speed_hz = 2000000
        self.spi.mode = 0b00
        self.init()

    def init(self):
#        while 1:
        mod = self.readReg(WHO_AM_I)
        if (mod==0xD3):
            print ("good")
        else:
            print("bad")

        # write 0 into REG3
        self.writeReg(CTRL_REG1, 0x0F)
        self.writeReg(CTRL_REG2, 0x00)
        self.writeReg(CTRL_REG3, 0x08)
        self.writeReg(CTRL_REG4, 0x30)
        self.writeReg(CTRL_REG5, 0x00)
        print (self.int2)


    def __stopSPI(self):
        self.spi.close()   
    

    def writeReg(self, reg, value):
            self.spi.xfer2([reg & 0x7F, value])
 #           self.spi.xfer([value])

    def readReg(self, reg):
            temp = self.spi.xfer2([reg | 0x80, 00])
            return temp[1]
               
    def readX(self):
            w = (self.readReg(0x29) & 0xFF) << 8
            w |= (self.readReg(0x28) & 0xFF)
            return self.twos_comp(w, 16)

    def readY(self):
            w = (self.readReg(0x2B) & 0XFF) << 8  #read y
            w |= (self.readReg(0x2A) & 0xFF)  
            return self.twos_comp(w, 16)


    def readZ(self):
            w = (self.readReg(0x2D) & 0XFF) << 8  #read z
            w |= (self.readReg(0x2C) & 0xFF)  
            return self.twos_comp(w, 16)   

    def readTemp(self):
            w = (self.readReg(0x26) & 0XFF)  #read temp 
            return self.twos_comp(w, 8)   

        
    def readInt1(self):
	    return self.int1

    def readInt2(self):
            return self.int2 
 
    def cleanup(self):
            self.__stopSPI()

    def twos_comp(self, val, bits):
        """compute the 2's complement of int value val"""
        if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << bits)        # compute negative value
        return val                         # return positive value as is

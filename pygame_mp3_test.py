import time
from pygame import mixer
import spidev
import RPi.GPIO as GPIO

spi_ch = 0

#Enable SPI
spi = spidev.SpiDev(0, spi_ch)
spi.max_speed_hz = 1200000

def translate(value, leftMin, leftMax, rightMin, rightMax):
    #Figure out how wide each range is
    leftSpan = leftMax-leftMin
    rightSpan = rightMax-rightMin

    #Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    #Convert the 01 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def read_adc(adc_ch, vref = 3.3):

    #Make sure ADC channel is 0 or 1
    if adc_ch != 0:
        adc_ch = 1

    #Construct SPI message
        #First bit (Start): Logic high (1)
        #Second bit (SGL/DIFF): 1 to select single mode
        #Thid bit (ODD/SIGN): Select channel (0 or 1)
        #Fourth bit (MSFB): 0 for LSB first
        #Next 12 bits: 0 (don't care)
    msg = 0b11
    msg = ((msg << 1) + adc_ch) << 5
    msg = [msg, 0b00000000]
    reply = spi.xfer2(msg)

    # Construct single integer out of the reply (2 bytes)
    adc = 0
    for n in reply:
        adc = (adc << 8) + n

    # Last bit (0) is not part of ADC value, shift to remove it
    adc = adc >> 1

    # Calculate voltage form ADC value
    voltage = (vref * adc) / 1024

    return voltage

# Report the channel 0 and channel 1 voltages to the terminal
mixer.init()

sound = mixer.Sound('/home/pi/Documents/The Beach Boys - Come Go With Me (2016 Remaster).wav')

sound.play()
mixer.pause()
curr_state = 0

try:
    while True:
        adc_0 = read_adc(0)
        scaled_adc_0 = (1/(adc_0)*10)**4 ## div by 0 error if sensor not plugged in
        print("Ch 0:", scaled_adc_0, "V")
        
        if (scaled_adc_0 > 94) and (curr_state == 0):
            mixer.unpause()
            curr_state = 1
        elif (scaled_adc_0 <= 95) and (curr_state == 1):
            mixer.pause()
            curr_state = 0

finally:
    GPIO.cleanup()



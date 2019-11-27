import time
import spidev
import matplotlib.pyplot as plt
import datetime as dt
from matplotlib.animation import FuncAnimation

spi_ch = 0

#Enable SPI
spi = spidev.SpiDev(0, spi_ch)
spi.max_speed_hz = 1200000

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

#Create figure for plotting
xs = []
ys = []
fig= plt.figure()
line, = plt.plot_date(xs, ys, '-')

def update(frame):
    # Read the value from ADC (getting value from cap sensors)
    adc_0 = read_adc(0)
    scaled_adc_0 = (1/(adc_0)*10)**4 ## div by 0 error if sensor not plugged in
    #adc_1 = read_adc(1)
    print("Ch 0:", scaled_adc_0, "V")
    
    # Add x and y to lists
    xs.append(dt.datetime.now())
    ys.append(scaled_adc_0)
    line.set_data(xs, ys)
    fig.gca().relim()
    fig.gca().autoscale_view()
    return line,

animation = FuncAnimation(fig, update, interval=100)
plt.show()

#finally:
#    GPIO.cleanup()



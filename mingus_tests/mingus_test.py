from mingus.midi import fluidsynth
import time
DEF_FONT_PATH = "/usr/share/sounds/sf2/FluidR3_GM.sf2"

#initialize General Midi soundfont
fluidsynth.init(DEF_FONT_PATH, 'alsa')
#time.sleep(0.25)

fluidsynth.play_Note(60,1,100)
fluidsynth.play_Note(65,1,100)
fluidsynth.play_Note(69,1,100)
time.sleep(1)
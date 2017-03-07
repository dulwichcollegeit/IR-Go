#!/usr/bin/python
# 
#   Python 2
#
#   IR-Go Main Program
#
#   Dulwich College Lower School Robotics and Coding!!!

from pocketsphinx import *
from sphinxbase import *
import pyaudio
import time
from subprocess import call
import RPi.GPIO as GPIO


#   Set pins for LEDs
Blue_LED_20 = 20
Red_LED_21 = 21

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(Blue_LED_20, GPIO.OUT)
GPIO.setup(Red_LED_21, GPIO.OUT)


#   Setup CMU PocketSphinx config
hmm = 'cmusphinx-5prealpha-en-us-ptm-2.0/'
dic = 'dictionary.dic'
lm = 'language_model.lm'
grammar = 'grammar.jsgf'

config = Decoder.default_config()
config.set_string('-hmm', hmm)
config.set_string('-dict', dic)
# Couldn't get grammar file to work
#config.set_string('-jsgf', grammar)
config.set_string('-lm', lm)    
bitesize = 1024 * 4
decoder = Decoder(config)
exit_program = False
action = []

while not exit_program:
    #   Get Audio from USB Mic
    pyAudio = pyaudio.PyAudio()
    stream = pyAudio.open(format=pyaudio.paInt16,
                                       channels=1,
                                       rate=16000,
                                       input=True,
                                       frames_per_buffer=bitesize)

    print "Speak"
    # Turn on Blue LED when ready to listen
    GPIO.output(Blue_LED_20, GPIO.HIGH)
    # Start an 'utterance'
    
    utteranceStarted = False
    utteranceEnded = False
    decoder.start_utt()
    # Get input
    while not utteranceEnded:
        try: # bypass any audio stream errors
            soundBite = stream.read(bitesize)
        except Exception:
            pass
        if soundBite:
            
            # Process a soundbite
            decoder.process_raw(soundBite, False, False)
            inSpeech = decoder.get_in_speech()
            
            if inSpeech and not utteranceStarted:
                utteranceStarted = True
                # Turn off blue LED
                GPIO.output(Blue_LED_20, GPIO.LOW)
            # The following checks for the transition from speech to silence.
            if not inSpeech and utteranceStarted:
                
                # End the utterance when the user finishes speaking
                utteranceEnded = True
                utteranceStarted = False
                try: 
                    decoder.end_utt()
                except Exception:
                    pass

                # Retrieve the hypothesis 
        
                hypothesis = decoder.hyp()
                if hypothesis is not None:
                    # Get the text of the hypothesis
                    bestGuess = hypothesis.hypstr
                    # Print out what was said
                    print 'I just heard you say:"{}"'.format(bestGuess)
                    stream.stop_stream()    
                    stream.close()

                    # Convert speech to Remote Control action
                    validCommand = 0
        	    if "ERGO" in bestGuess:
			if "PROJECTOR" in bestGuess:
			    if "POWER" in bestGuess:
                                action = ["irsend", "SEND_ONCE", "PICOPIX", "KEY_POWER"]
                            elif "BRIGHTNESS UP" in bestGuess:
                                action = ["irsend", "SEND_ONCE", "PICOPIX", "KEY_BRIGHTNESSUP"]
                            elif "BRIGHTNESS DOWN" in bestGuess:
                                action = ["irsend", "SEND_ONCE", "PICOPIX", "KEY_BRIGHTNESSDOWN"]
                            elif "VOLUME UP" in bestGuess:
                                action = ["irsend", "SEND_ONCE", "PICOPIX", "KEY_VOLUMEUP"]
                            elif "VOLUME DOWN" in bestGuess:
                                action = ["irsend", "SEND_ONCE", "PICOPIX", "KEY_VOLUMEDOWN"]
                            elif "UP" in bestGuess:
                                action = ["irsend", "SEND_ONCE", "PICOPIX", "KEY_UP"]
                            elif "DOWN" in bestGuess:
                                action = ["irsend", "SEND_ONCE", "PICOPIX", "KEY_DOWN"]
                            elif "OKAY" in bestGuess:
                                action = ["irsend", "SEND_ONCE", "PICOPIX", "KEY_OK"]
                            elif "MUTE" in bestGuess:
                                action = ["irsend", "SEND_ONCE", "PICOPIX", "KEY_MUTE"]
                            elif "ZOOM" in bestGuess:
                                action = ["irsend", "SEND_ONCE", "PICOPIX", "KEY_ZOOM"]
                            elif "FAST FORWARD" in bestGuess:
                                action = ["irsend", "SEND_ONCE", "PICOPIX", "KEY_FASTFORWARD"]
                            elif "REWIND" in bestGuess:
                                action = ["irsend", "SEND_ONCE", "PICOPIX", "KEY_REWIND"]
                            elif "PLAY" in bestGuess:
                                action = ["irsend", "SEND_ONCE", "PICOPIX", "KEY_PLAY"]
                            elif "BACK" in bestGuess:
                                action = ["irsend", "SEND_ONCE", "PICOPIX", "KEY_BACK"]
                            elif "LEFT" in bestGuess:
                                action = ["irsend", "SEND_ONCE", "PICOPIX", "KEY_LEFT"]
                            elif "RIGHT" in bestGuess:
                                action = ["irsend", "SEND_ONCE", "PICOPIX", "KEY_RIGHT"]
                            else:
                                validCommand = 2
                        elif bestGuess == "ERGO ERGO":
                            if len(action) != 4:
                                validCommand = 1
                            else:
                                print "Repeat: " + action[3]
                        elif bestGuess == "ERGO EXIT EXIT":
                                exit_program = True
                                validCommand = 3
                        else:
                            validCommand = 2
                        if validCommand == 0:
                            call(action)
                    else:
                        validCommand = 2
                    if validCommand > 0:
                        print "Error"
                        for flash in range(validCommand): # Number of flashes
                            time.sleep(0.5)
                            GPIO.output(Red_LED_21, GPIO.HIGH)
                            time.sleep(0.5)
                            GPIO.output(Red_LED_21, GPIO.LOW)
                    
                                    




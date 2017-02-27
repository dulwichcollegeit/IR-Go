#!/usr/bin/python
# 
#   Python 2?
#
#   IR-Go Main Program

from pocketsphinx import *
from sphinxbase import *
import pyaudio
import time
from subprocess import call

hmm = 'cmusphinx-5prealpha-en-us-ptm-2.0/'
dic = 'dictionary.dic'
lm = 'language_model.lm'
grammar = 'grammar.jsgf'

config = Decoder.default_config()
config.set_string('-hmm', hmm)
config.set_string('-dict', dic)
#config.set_string('-jsgf', grammar)
config.set_string('-lm', lm)    
bitesize = 1024 * 4
#config.set_boolean("-allphone_ci", True)
decoder = Decoder(config)
exit_program = False

while not exit_program:
    pyAudio = pyaudio.PyAudio()
    stream = pyAudio.open(format=pyaudio.paInt16,
                                       channels=1,
                                       rate=16000,
                                       input=True,
                                       frames_per_buffer=bitesize)

    print "Speak"
    # Turn on Speak LED

    # Start an 'utterance'
    
    utteranceStarted = False
    utteranceEnded = False
    decoder.start_utt()
    # Get input
    while not utteranceEnded:
        try:
            soundBite = stream.read(bitesize)
        except Exception:
            pass
       #print "Got soundbite"
        if soundBite:
            
            # Process a soundbite
            decoder.process_raw(soundBite, False, False)
            inSpeech = decoder.get_in_speech()
            
            if inSpeech and not utteranceStarted:
                utteranceStarted = True
                # Turn off Speak LED
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
               # print utteranceEnded
                hypothesis = decoder.hyp()
                if hypothesis is not None:
                    # Get the text of the hypothesis
                    bestGuess = hypothesis.hypstr
                    # Print out what was said
                  #  bestGuess = bestGuess.replace('ERGO ', '')
                  #  bestGuess = bestGuess.replace(' ERGO', '')
                    print 'I just heard you say:"{}"'.format(bestGuess)
                    stream.stop_stream()    
                    stream.close()



        
                    if "POWER" in bestGuess:
                        call(["irsend", "SEND_ONCE", "PICOPIX", "KEY_POWER"])
                    elif "OK" in bestGuess:
                        call(["irsend", "SEND_ONCE", "PICOPIX", "KEY_OK"])
                    elif "LEFT" in bestGuess:
                        call(["irsend", "SEND_ONCE", "PICOPIX", "KEY_LEFT"])
                    elif "RIGHT" in bestGuess:
                        call(["irsend", "SEND_ONCE", "PICOPIX", "KEY_RIGHT"])
                    elif bestGuess == "ERGO EXIT":
                        exit_program = True
                    else:
                        print "Error"
                    #time.sleep(2)






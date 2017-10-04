
#!/usr/bin/env python

import RPi.GPIO as GPIO
import mfrc522.MFRC522 as MFRC522
import signal

class MfcReader():
    def __init__(self):
        self.continue_reading = True
        signal.signal(signal.SIGINT, self.end_read)
        self.MIFAREReader = MFRC522.MFRC522()

        return

    def read_card(self):
        uid = None
        while self.continue_reading:
            # Scan for cards    
            (status,TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)

            # If a card is found
            if status == self.MIFAREReader.MI_OK:
                #print("Card detected")
                pass
            
            # Get the UID of the card
            (status,uid) = self.MIFAREReader.MFRC522_Anticoll()

            # If we have the UID, continue
            if status == self.MIFAREReader.MI_OK:

                # Print UID
                #print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
            
                # This is the default key for authentication
                key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
                
                # Select the scanned tag
                self.MIFAREReader.MFRC522_SelectTag(uid)

                # Authenticate
                status = self.MIFAREReader.MFRC522_Auth(self.MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

                # Check if authenticated
                if status == self.MIFAREReader.MI_OK:
                    self.MIFAREReader.MFRC522_Read(8)
                    self.MIFAREReader.MFRC522_StopCrypto1()
                else:
                    print("Authentication error")

                break

        GPIO.cleanup()
        return uid[0] + uid[1] + uid[2] + uid[3]
        

    def end_read(self, signal, frame):
        #print "Ctrl+C captured, ending read."
        self.continue_reading = False
        GPIO.cleanup()
        return




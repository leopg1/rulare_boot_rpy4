import RPi.GPIO as GPIO
import time

# Definire GPIO-uri pentru puntea H
GPIO_AB_1 = 5   # A
GPIO_AB_2 = 6   # B
GPIO_CD_1 = 19  # C
GPIO_CD_2 = 26  # D

# Inițializare GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setăm pinii ca OUTPUT și LOW la pornire
motor_pins = [GPIO_AB_1, GPIO_AB_2, GPIO_CD_1, GPIO_CD_2]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)  # Asigurăm că pinii PORNESC LOW

# Timp mort între schimbările de direcție
DELAY_SEC = 3

def motor_inainte():
    """Activează motorul înainte (AB) cu protecție"""
    oprire_motoare()
    time.sleep(DELAY_SEC)
    GPIO.output(GPIO_AB_1, GPIO.HIGH)
    GPIO.output(GPIO_AB_2, GPIO.HIGH)

def motor_inapoi():
    """Activează motorul înapoi (CD) cu protecție"""
    oprire_motoare()
    time.sleep(DELAY_SEC)
    GPIO.output(GPIO_CD_1, GPIO.HIGH)
    GPIO.output(GPIO_CD_2, GPIO.HIGH)

def oprire_motoare():
    """Oprește toate motoarele și resetează GPIO-urile"""
    print("🛑 Oprire motoare și resetare GPIO-uri la LOW...")
    for pin in motor_pins:
        GPIO.output(pin, GPIO.LOW)

def cleanup_gpio():
    """Asigură resetarea GPIO-urilor"""
    oprire_motoare()
    time.sleep(DELAY_SEC)  # Mică întârziere pentru siguranță
    GPIO.cleanup()

# Testare comenzi
if __name__ == "__main__":
    try:
        print("Pornire motor înainte...")
        motor_inainte()
        time.sleep(DELAY_SEC)
        
        print("Oprire...")
        oprire_motoare()
        time.sleep(DELAY_SEC)
        
        print("Pornire motor înapoi...")
        motor_inapoi()
        time.sleep(DELAY_SEC)
        
        print("Oprire finală...")
        oprire_motoare()

    except KeyboardInterrupt:
        print("\n🔴 Oprire de urgență!")
        cleanup_gpio()
    finally:
        cleanup_gpio()

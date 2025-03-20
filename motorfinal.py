import RPi.GPIO as GPIO
import requests
import time

# Configurare GPIO pentru ambele motoare
MOTOR1_FORWARD = [5, 6]   # GPIO-uri pentru mers înainte motor 1
MOTOR1_BACKWARD = [19, 26] # GPIO-uri pentru mers înapoi motor 1

MOTOR2_FORWARD = [4, 14]   # GPIO-uri pentru mers înainte motor 2
MOTOR2_BACKWARD = [22, 24] # GPIO-uri pentru mers înapoi motor 2

ALL_MOTOR_PINS = MOTOR1_FORWARD + MOTOR1_BACKWARD + MOTOR2_FORWARD + MOTOR2_BACKWARD

# API-ul de unde citim statusul motoarelor
API_URL = "http://207.154.237.32:5000/motor_status"

# Timp mort între schimbarea direcției pentru a proteja puntea H
DELAY_SEC = 0.1  # 100ms

# Inițializare GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setăm toate GPIO-urile pe OUTPUT și LOW la start
for pin in ALL_MOTOR_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Funcții pentru controlul motoarelor
def motor1_inainte():
    """Activează motorul 1 înainte"""
    oprire_motor1()
    time.sleep(DELAY_SEC)
    GPIO.output(MOTOR1_FORWARD[0], GPIO.HIGH)
    GPIO.output(MOTOR1_FORWARD[1], GPIO.HIGH)

def motor1_inapoi():
    """Activează motorul 1 înapoi"""
    oprire_motor1()
    time.sleep(DELAY_SEC)
    GPIO.output(MOTOR1_BACKWARD[0], GPIO.HIGH)
    GPIO.output(MOTOR1_BACKWARD[1], GPIO.HIGH)

def oprire_motor1():
    """Oprește motorul 1"""
    GPIO.output(MOTOR1_FORWARD[0], GPIO.LOW)
    GPIO.output(MOTOR1_FORWARD[1], GPIO.LOW)
    GPIO.output(MOTOR1_BACKWARD[0], GPIO.LOW)
    GPIO.output(MOTOR1_BACKWARD[1], GPIO.LOW)

def motor2_inainte():
    """Activează motorul 2 înainte"""
    oprire_motor2()
    time.sleep(DELAY_SEC)
    GPIO.output(MOTOR2_FORWARD[0], GPIO.HIGH)
    GPIO.output(MOTOR2_FORWARD[1], GPIO.HIGH)

def motor2_inapoi():
    """Activează motorul 2 înapoi"""
    oprire_motor2()
    time.sleep(DELAY_SEC)
    GPIO.output(MOTOR2_BACKWARD[0], GPIO.HIGH)
    GPIO.output(MOTOR2_BACKWARD[1], GPIO.HIGH)

def oprire_motor2():
    """Oprește motorul 2"""
    GPIO.output(MOTOR2_FORWARD[0], GPIO.LOW)
    GPIO.output(MOTOR2_FORWARD[1], GPIO.LOW)
    GPIO.output(MOTOR2_BACKWARD[0], GPIO.LOW)
    GPIO.output(MOTOR2_BACKWARD[1], GPIO.LOW)

# Funcția principală care verifică API-ul și controlează motoarele
def verificare_si_control():
    while True:
        try:
            response = requests.get(API_URL)
            data = response.json()

            motor1_status = data.get("motor1", "oprit")
            motor2_status = data.get("motor2", "oprit")

            # Control Motor 1
            if motor1_status == "inainte":
                motor1_inainte()
            elif motor1_status == "inapoi":
                motor1_inapoi()
            else:
                oprire_motor1()

            # Control Motor 2
            if motor2_status == "inainte":
                motor2_inainte()
            elif motor2_status == "inapoi":
                motor2_inapoi()
            else:
                oprire_motor2()

            # Așteaptă 1 secundă înainte de a verifica din nou API-ul
            time.sleep(1)

        except Exception as e:
            print(f"Eroare la verificare API: {e}")
            time.sleep(2)  # Dacă apare o eroare, așteptăm 2 secunde înainte de a reîncerca

# Pornire proces de verificare și control
if __name__ == "__main__":
    try:
        print("🔄 Pornire control motoare...")
        verificare_si_control()
    except KeyboardInterrupt:
        print("\n🛑 Oprire de urgență! Curățare GPIO...")
        oprire_motor1()
        oprire_motor2()
        GPIO.cleanup()

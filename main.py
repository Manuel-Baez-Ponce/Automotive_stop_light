# importar los paquetes necesarios de la libreria machine y time
from machine import ADC, Pin, PWM
from time import sleep as delay

# Configurar el pin del modulo LDR o fotoresistencia
ldr = Pin(17, Pin.IN, Pin.PULL_DOWN)
pedal = Pin(27, Pin.IN, Pin.PULL_DOWN)

# Configurar el ADC en el pin GP26 (canal 0)
potenciometro = ADC(Pin(26))

# Configurar el PWM en el pin GP16
faro = PWM(Pin(16))
faro.freq(1000)  # Frecuencia de 1 kHz

def leerADC():
    # retornar el valor leido del adc
    return potenciometro.read_u16()

def escribirPWM(ciclo):
    # Adaptar el valor para el PWM utilizando casteo int()
    if (ciclo < 65536):	# limitar el valor de ciclo al valor maximo del registro
        faro.duty_u16(int(ciclo))
    else:
        faro.duty_u16(65535)
    return

def main():
    print("Programa de control para faro automotriz.")
    while True:
        # Leer el valor del ADC de 16 bits en un rango de valores de (0-65535)
        potValor = leerADC() - 400 # se corrige la desviación estandar de la lectura
        # Adaptar el valor para mostrarlo por consola
        faroPorcentage = int((potValor/65535)*100) 
        print(f"valor leido del adc: {potValor}, ciclo de trabajo del pwm: {faroPorcentage}%")
        # Leer el valor del sensor fotorresistencia y el pedal de freno
        if pedal.value():	# Al momento de accionar el pedal el faro enciende en su totalidad
            escribirPWM(65535)
        elif not ldr.value(): # Si el LDR detecta que hay luz ambiental apaga el faro
            escribirPWM(0)  
        else:   # En caso contrario el faro enciende controlado por el potenciometro
            escribirPWM(potValor)
        delay(0.1) # retardo de 100ms

if __name__=='__main__':
    main()
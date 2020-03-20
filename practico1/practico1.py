def adivinar(nro_intentos):
    import random
    numero_random = random.randint(0, 100)
    nro_intentos_actual=0
    nro_intentos_restantes=0
    print ("El numero random es " + str(numero_random))

    while True:
        numero_ingresado = int(input("Ingrese un numero entre 0 y 100 "))
        while (numero_ingresado < 0 or numero_ingresado > 100):
            print ("El numero ingrsado " + str(numero_ingresado) + " no esta dentro del rango requerido")
            numero_ingresado = int(input("Ingrese un numero entre 0 y 100 "))
        else:
            print ("El numero ingresado es " + str(numero_ingresado))
            nro_intentos_actual = nro_intentos_actual + 1
            nro_intentos_restantes = nro_intentos - 1
            if (numero_ingresado != numero_random):
                print("NO ADIVINASTE!")

                print("Te quedan " + str(nro_intentos_restantes) + " intentos")
            if nro_intentos_restantes == 0:
                print("NO ACERTASTE EN NINGUN INTENTO")
                break
            else:
                print("ACERTASTE!! fue en el intento " + str(nro_intentos_actual))
                break

print("PROGRAMA ADIVINADOR")
print("PROGRAMA ADIVINADOR")
intentos=int(input("Ingrese el numero de intentos "))
adivinar(intentos)
print("GAME OVER")


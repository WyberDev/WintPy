# Setup ────────────────────────────────────────────
import os
import platform
import time
import socket

py_location = os.path.dirname(os.path.abspath(__file__))
carpeta_actual = os.path.dirname(os.path.abspath(__file__))
os.chdir(carpeta_actual)
tiempo_en_iniciar = time.time()

# Boot ─────────────────────────────────────────────

print("¡Bienvenido a \033[34mWint\033[33mPy\033[33m\033[0m!")
print("Escribe --help para ayuda.")

# Sandbox ──────────────────────────────────────────

SANDBOX_ROOT = os.getcwd()
sandbox_activo = True
carpeta_padre = os.path.abspath(os.path.join(os.getcwd(), ".."))
# print(os.path.abspath(os.path.join(os.getcwd(), "..")))

while sandbox_activo == False:
    carpeta_padre = False


# Misc ─────────────────────────────────────────────

# Colors ───────────────────────────────────────────

# RESET = "\033[0m"
# ROJO = "\033[31m"
# VERDE = "\033[32m"
# AMARILLO = "\033[33m"
# AZUL = "\033[34m"
# MAGENTA = "\033[35m"
# CIAN = "\033[36m"
# BLANCO = "\033[37m"
# GRIS = "\033[90m"

# Usage ────────────────────────────────────────────

while True:
    comando = input().lower()
    if comando == "--help":
        print("\033[33m--help = Muestra esta ventana.\033[0m")
        print("mkdir = Crea un directorio.")
        print("rmdir = Elimina un directorio.")
        print("mkfle = Crea un archivo.")
        print("rm = Elimina un archivo.")
        print("cd = Abrir un directorio.")
        print("cd .. = Retrocede un directorio atrás.")
        print("ls = Muestra los directorios y archivos en los que estás.")
        print("exit = Salir.")
        print("clear = Limpia todo el texto.")
        print("refetch = Muestra información del sistema y hardware.")
        print("disa = \033[31m(¡No recomendado!)\033[0m Desactiva el sandboxing y permite interactuar con el sistema.")
        print("ensa = Activa el sandbox \033[90m(Si lo desactivaste anteriormente)\033[0m")

    elif comando == "ls":
        print(os.listdir())
    elif comando == "mkdir":
        carpeta_nueva = input("Nombre del directorio: ")
        os.mkdir(carpeta_nueva)
    elif comando == "rmdir":
        remover_carpeta = input("Carpeta a remover: ")
        os.rmdir(remover_carpeta)
    elif comando == "cd":
        try:
            ir_a = input("Ir a directorio: ")
            os.chdir (ir_a)
            print(os.getcwd())
        except FileNotFoundError:
            print("cd: El directorio no existe.")
    
    elif comando == "cd ..":    
        carpeta_padre = os.path.abspath(os.path.join(os.getcwd(), ".."))

        if sandbox_activo and not carpeta_padre.startswith(SANDBOX_ROOT):
            print("cd: no se puede retroceder más")
        else:
            try:
                os.chdir("..")
            except FileNotFoundError:
                print("cd: no se puede retroceder más.")

    elif comando == "exit":
        print("Cerrando WintPy")
        break
    elif comando == "rm":
        remover = input("Archivo a remover: ")
        os.remove(remover)
    elif comando == "clear":
        os.system('cls' if os.name == 'nt' else 'clear')
    
    elif comando == "disa":
        lock1 = input("\033[31mVas a desactivar el sandboxing\033[0m, esto puede ser peligroso ¿Continuar? (Si / No) ").strip()
        if lock1 == "Si":
            lock2 = input("¿Estás seguro? ").strip()
            if lock2 == "Si":
                sandbox_activo = False
                print("Sandbox desactivado, ten cuidado")

    elif comando == "ensa":
        if sandbox_activo == True:
            print("El sandbox esta activado")
        elif sandbox_activo == False:
            os.chdir(carpeta_actual)
            sandbox_activo = True
            carpeta_padre = os.path.abspath(os.path.join(os.getcwd(), ".."))
            print("Sandbox activado de vuelta.")  
#            if sandbox_activo and not carpeta_padre.startswith(SANDBOX_ROOT):

    elif comando == "mkfle":
        mkfle = input("Nombre del archivo y formato (No poner formato para un archivo simple):")
        try:
            with open(mkfle, "x") as archivo:
                pass
            print("Archivo creado.")      
        except FileExistsError:
            print("[Error] Ese archivo ya existe en esta carpeta.")
    elif comando == "refetch":
        segundos_totales = int(time.time() - tiempo_en_iniciar)
        minutos = segundos_totales // 60
        segundos = segundos_totales % 60
        if minutos > 0:
            texto_uptime = f"{minutos} min, {segundos} seg"
        else:
            texto_uptime = f"{segundos} seg"
        info = [
            "\033[34mWint\033[33mPy\033[0m OS 1.0.0 Base",
            "-------------------------",
            f"SO Base: {platform.system()} {platform.release()}",
            f"Nombre del usuario: {socket.gethostname()}",
            f"Uptime: {texto_uptime}",
#            f"Display:" {platform.disp} platform
            f"\033[32mHola!\033[0m"
            ]
        for linea in info:
            print(linea)
    else:
        print("Comando desconocido")
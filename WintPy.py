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

print("¡Welcome to \033[34mWint\033[33mPy\033[33m\033[0m!")
print("Write -h for help.")

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
    if comando == "-h":
        print("\033[33m-h = Shows this window.\033[0m")
        print("mkdir = Create a directory.")
        print("rmdir = Delete a directory.")
        print("mkfle = Create a file.")
        print("rm = Delete a file.")
        print("cd = Open a directory.")
        print("cd .. = Get back one directory.")
        print("ls = Shows directory and files where you in.")
        print("exit = Exit.")
        print("clear = Clean all text on screen.")
        print("refetch = Shows info about system and hardware.")
        print("disa = \033[31m(¡Not recommended!)\033[0m Disables sandboxing and lets you interact with the system.")
        print("ensa = Enable the sandbox \033[90m(If you disabled it previously)\033[0m")

    elif comando == "ls":
        print(os.listdir())
    elif comando == "mkdir":
        carpeta_nueva = input("Name of the directory: ")
        os.mkdir(carpeta_nueva)
    elif comando == "rmdir":
        remover_carpeta = input("Folder to remove: ")
        os.rmdir(remover_carpeta)
    elif comando == "cd":
        try:
            ir_a = input("Go to directory: ")
            os.chdir (ir_a)
            print(os.getcwd())
        except FileNotFoundError:
            print("cd: Directory doesn't exist.")
    
    elif comando == "cd ..":    
        carpeta_padre = os.path.abspath(os.path.join(os.getcwd(), ".."))

        if sandbox_activo and not carpeta_padre.startswith(SANDBOX_ROOT):
            print("cd: it cannot go back")
        else:
            try:
                os.chdir("..")
            except FileNotFoundError:
                print("cd: it cannot go back.")

    elif comando == "exit":
        print("Closing WintPy")
        break
    elif comando == "rm":
        remover = input("File to remove: ")
        os.remove(remover)
    elif comando == "clear":
        os.system('cls' if os.name == 'nt' else 'clear')
    
    elif comando == "disa":
        lock1 = input("\033[31mYou are going to disable the sandboxing\033[0m, This can be harmful ¿Continue? ( Yes / No ) ").strip()
        if lock1 == "Yes":
            lock2 = input("¿Are you sure? ").strip()
            if lock2 == "Yes":
                sandbox_activo = False
                print("Sandbox disabled, have care")

    elif comando == "ensa":
        if sandbox_activo == True:
            print("Sandbox already enabled")
        elif sandbox_activo == False:
            os.chdir(carpeta_actual)
            sandbox_activo = True
            carpeta_padre = os.path.abspath(os.path.join(os.getcwd(), ".."))
            print("Sandbox enabled again.")  
#            if sandbox_activo and not carpeta_padre.startswith(SANDBOX_ROOT):

    elif comando == "mkfle":
        mkfle = input("Name of the file and format (write without format for a simple file):")
        try:
            with open(mkfle, "x") as archivo:
                pass
            print("File created.")
        except FileExistsError:
            print("[Error] File already exists on this folder.")
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
            f"Base OS: {platform.system()} {platform.release()}",
            f"User name: {socket.gethostname()}",
            f"Uptime: {texto_uptime}",
#            f"Display:" {platform.disp} platform
            f"\033[32mHi!\033[0m"
            ]
        for linea in info:
            print(linea)
    else:
        print("Unknown command")
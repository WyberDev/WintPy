# WintPy Main v1.0.4
# Setup ────────────────────────────────────────────
import os, platform, time, socket, urllib.request, json, subprocess, sys, shutil, termios, tty

py_location = os.path.dirname(os.path.abspath(__file__))
carpeta_actual = os.path.dirname(os.path.abspath(__file__))
os.chdir(carpeta_actual)
tiempo_en_iniciar = time.time()
os.makedirs("packages", exist_ok=True)
os.makedirs("users", exist_ok=True)

usuarioscarpeta = "users"
contenido_usuario = os.listdir(usuarioscarpeta)
dev = False
archivo_en_portapapeles = ""
newuser = True
skipuser = False
newuserfrommk = False
working = True
passtologout = False
commandlogout = False
innovatorrunning = False
user1name = ""
users = []
if len(contenido_usuario) > 0:
    newuser = False
de = "Consola"

# Boot ─────────────────────────────────────────────

print("¡Bienvenido a \033[34mWint\033[33mPy\033[33m\033[0m!")
if newuser == True:
    print("¿Es tu primera vez? ¿Quieres crear un usuario? (Escribe G para entrar como invitado, S para no mostrar esto la próxima vez.)")
    user1name = input("\033[33mNombre del usuario: \033[0m")
    if user1name == "G":
        newuser = False
        print("Entrando como invitado")

    elif user1name == "S":
        print("Entrando como invitado")
        print("En caso de que quiera crear un usuario, \033[033mhazlo con mkuser\033[0m")
        skipuser = True
        newuser = False

    elif user1name != "G":
        users.append(user1name)
        make_folder_user = os.path.join(usuarioscarpeta, user1name)
        package_user_folder = os.path.join(make_folder_user, "packages")
        personalthings = input("¿Deseas integrar carpetas de paquetes para el usuario? (si / no) ").lower()
        if personalthings == "si":
            os.makedirs(make_folder_user, exist_ok=True)
            os.makedirs(package_user_folder, exist_ok=True)
        elif personalthings == "no":
            os.makedirs(make_folder_user, exist_ok=True)

print("Escribe \033[35m--help\033[0m para ayuda.")

# Sandbox ──────────────────────────────────────────

SANDBOX_ROOT = os.getcwd()
sandbox_activo = True
carpeta_padre = os.path.abspath(os.path.join(os.getcwd(), ".."))
# print(os.path.abspath(os.path.join(os.getcwd(), "..")))

while sandbox_activo == False:
    carpeta_padre = False

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

re = "\033[0m"
ro = "\033[31m"
ve = "\033[32m"
az = "\033[34m"
am = "\033[33m"
ma = "\033[35m"
ci = "\033[36m"
bl = "\033[37m"
gr = "\033[90m"

# Misc ─────────────────────────────────────────────

wintpy_logo = fr"""
    {bl}    ..................{az}__{am}____{bl}.....
    {bl}..............{az}__{bl}.{az}/{bl}.{am}___oo\{bl}....
    {bl}..{az}___{bl}........{az}/##/{bl}.{am}/s  \oo\{bl}...
    {bl}..{az}\##\{bl}..{az}/\{bl}..{az}/##/{bl}.{am}/ss__/oo/{bl}...
    {bl}...{az}\##\/##\/##/{bl}.{am}/##/____/{bl}....
    {bl}....{az}\########/{bl}.{am}/dd/{bl}..........
    .....{az}\##/\##/{bl}.{am}/dd/{bl}...........
    ......{az}\/{bl}..{az}\/{bl}.{am}/dd/{bl}............
    ............{am}/dd/{bl}.............
    {bl}...........{am}/__/{bl}..............
    {re}
    """

commands = ["--help", "mkdir", "mkfle", "rmdir", "rm", "cd", "cp", "pt", "ls",
                "edit", "exit", "clear", "refetch", "logout", "devmode", "mkuser",
                "pkg -list", "pkg -remove", "exec", "disa", "ensa"]

# Functions ────────────────────────────────────────

def obtener_lista_paquetes():
    url_api = "https://api.github.com/repos/WyberDev/WintPy-Packages-Repository/contents/"
    peticion = urllib.request.Request(url_api, headers={'User-Agent': 'WintPy-OS-Package-Manager'})
    with urllib.request.urlopen(peticion) as respuesta:
        datos_crudos = respuesta.read().decode("utf-8")
    elementos = json.loads(datos_crudos)
    return [item["name"] for item in elementos if item["type"] == "dir"]

def menu(lista_paquetes):
    if not lista_paquetes:
        print("\nNo se encontraron paquetes en el repositorio.")
        return None
        
    print("\n📦 PAQUETES DISPONIBLES (Q para cancelar):")
    print("-" * 30)
    
    for i, pkg in enumerate(lista_paquetes, start=1):
        print(f" {i}. {pkg}")
    print("-" * 30)
    
    while True:
        opcion = input("Elige un número para instalar (o 'q' para cancelar): ").strip()
        
        if opcion.lower() == 'q':
            print("❌ Operación cancelada por el usuario.")
            return None
            
        if opcion.isdigit():
            numero = int(opcion)
            if 1 <= numero <= len(lista_paquetes):
                return lista_paquetes[numero - 1]
                
        print("⚠️ Opción inválida. Por favor, introduce un número de la lista.")

def descargar_paquete(nombre_paquete):
    nombre_paquete = str(nombre_paquete).strip()
    print(f"Conectando para instalar: {nombre_paquete}...")
    
    carpeta_destino = os.path.join("packages", nombre_paquete)
    os.makedirs(carpeta_destino, exist_ok=True)
    
    base_url_raw = f"https://raw.githubusercontent.com/WyberDev/WintPy-Packages-Repository/main/{nombre_paquete}"
    
    url_json = f"{base_url_raw}/info.json"
    ruta_json_local = os.path.join(carpeta_destino, "info.json")
    
    try:
        urllib.request.urlretrieve(url_json, ruta_json_local)
        
        with open(ruta_json_local, "r", encoding="utf-8") as f:
            configuracion = json.load(f)
        
        nombre_archivo_py = configuracion.get("main_file", "main.py").strip()
#        print(f" -> Detectado archivo principal en JSON: {nombre_archivo_py}")
        
        url_script_py = f"{base_url_raw}/{nombre_archivo_py}"
        ruta_py_local = os.path.join(carpeta_destino, nombre_archivo_py)
        urllib.request.urlretrieve(url_script_py, ruta_py_local)
        
        url_reqs = f"{base_url_raw}/requirements.txt"
        ruta_reqs_local = os.path.join(carpeta_destino, "requirements.txt")
        try:
            urllib.request.urlretrieve(url_reqs, ruta_reqs_local)
            print(" -> Requisitos del sistema detectados y descargados.")
        except Exception:
            pass

        print(f"¡Paquete '{nombre_paquete}' instalado con éxito!")
        
    except Exception as e:
        print(f"❌ Error durante la descarga de archivos: {e}")

def cp():
    global archivo_en_portapapeles
    # El usuario puede ingresar una ruta completa o solo el nombre si está en la misma carpeta
    ruta_origen = input("Introduce la ruta completa del archivo a copiar:\n> ")
    
    # os.path.abspath convierte cualquier ruta en la ruta real completa de tu sistema
    ruta_absoluta = os.path.abspath(ruta_origen)
    
    if os.path.exists(ruta_absoluta):
        archivo_en_portapapeles = ruta_absoluta
        print(f"\n¡Copiado al portapapeles!")
        print(f"Ruta guardada: {archivo_en_portapapeles}")
    else:
        print("No se encontró ningún archivo en esa ruta.")

def pt():
    global archivo_en_portapapeles
    
    if not archivo_en_portapapeles:
        print("No hay nada en el portapapeles.")
        return
        
    ruta_destino = input("\n¿Con qué nombre quieres pegarlo? (usa 'same' para reutilizar el nombre del archivo copiado):\n> ")
    
    if ruta_destino.strip().lower() == "same":
        nombre_original = os.path.basename(archivo_en_portapapeles)
        ruta_final = os.path.abspath(nombre_original)
    else:
        ruta_destino_absoluta = os.path.abspath(ruta_destino)
        
        if os.path.isdir(ruta_destino_absoluta):
            nombre_archivo = os.path.basename(archivo_en_portapapeles)
            ruta_final = os.path.join(ruta_destino_absoluta, nombre_archivo)
        else:
            ruta_final = ruta_destino_absoluta
    
    try:
        shutil.copy2(archivo_en_portapapeles, ruta_final)
        print(f"\n¡Pegado con éxito en: {ruta_final}")
        
    except shutil.SameFileError:
        print("Error: Estás intentando pegar el archivo en la misma carpeta de donde lo copiaste.")
    except FileNotFoundError:
        print("Error: La carpeta de destino no existe. Verifica bien la ruta.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def userscanning(usuarioscarpeta):
    # Si la ruta no existe, devuelve el array vacío directamente para evitar errores
    if not os.path.exists(usuarioscarpeta):
        return []
    
    # Escanea, filtra que sean carpetas (y no archivos u ocultas) y lo mete al array
    return [f.name for f in os.scandir(usuarioscarpeta) if f.is_dir() and not f.name.startswith('.')]

def chequear_reqs(ruta_app):
    ruta_txt = os.path.join(ruta_app, "requirements.txt")
        
    if not os.path.exists(ruta_txt): return True

    with open(ruta_txt, 'r') as f:
        reqs = [l.strip().split('==')[0].split('>=')[0] for l in f if l.strip() and not l.startswith('#')]

    faltan = []
    for r in reqs:
        try: 
            # RASTREADOR 2: Ver si Python cree que ya lo tiene
            __import__(r.lower())
        except ImportError: 
            faltan.append(r)

    if not faltan: return True

    print(f"⚠️ Faltan requisitos: {faltan}")
    if input("¿Instalar? (s/n): ").lower() not in ['s', 'si', 'y']: return False

    es_arch = os.path.exists("/etc/arch-release") or "arch" in platform.release().lower()
    map_arch = {"pygame": "python-pygame", "requests": "python-requests", "numpy": "python-numpy", "colorama": "python-colorama"}

    for mod in faltan:
        cmd = ["sudo", "pacman", "-Sy", map_arch[mod.lower()], "--noconfirm"] if (es_arch and mod.lower() in map_arch) else [sys.executable, "-m", "pip", "install", mod]
        try: subprocess.run(cmd, check=True)
        except Exception: subprocess.run([sys.executable, "-m", "pip", "install", mod, "--user"]) 
        
    return True

def buscar_sugerencia(texto_actual):
    """Busca en la lista de comandos cuál coincide con lo que va escrito."""
    if not texto_actual:
        return ""
    for cmd in commands:
        if cmd.startswith(texto_actual):
            return cmd
    return ""

def better_input(prompt="> "):
    """Captura las teclas una a una con autocompletado estilo Fish corregido."""
    print(prompt, end="", flush=True)
    entrada = ""
    
    while True:
        fd = sys.stdin.fileno()
        viejos_ajustes = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, viejos_ajustes)

        codigo = ord(char)
        
        if codigo in (13, 10):  # enter key
            print(f"\r\033[K{prompt}{entrada}", flush=True)
            break
            
        elif codigo == 127:  # backspace
            if len(entrada) > 0:
                entrada = entrada[:-1]
                
#        elif codigo == 3:  # CTRL + C
#            print("\n\n[ Proceso interrumpido. Saliendo de WintPy... ]")
#            sys.exit(0)
                
        elif codigo == 27:  # escape
            siguiente1 = sys.stdin.read(1)
            siguiente2 = sys.stdin.read(1)
            if siguiente1 == "[" and siguiente2 == "C":  # right key
                sugerencia = buscar_sugerencia(entrada)
                if sugerencia:
                    entrada = sugerencia

        elif 32 <= codigo <= 126:  # normal letters
            entrada += char

        print(f"\r\033[K{prompt}{entrada}", end="", flush=True)
        
        sugerencia = buscar_sugerencia(entrada)
        
        if sugerencia and entrada != "" and len(sugerencia) > len(entrada):
            resto = sugerencia[len(entrada):]
            print(f"\033[90m{resto}\033[0m", end="", flush=True)
            print(f"\033[{len(resto)}D", end="", flush=True)
            
    return entrada


# Usage ────────────────────────────────────────────
while working == True:
    passtologout = False

    comando = better_input("> ").lower()
    if comando == "--help":
        print("\033[33m--help = Muestra esta ventana.\033[0m")
        print("mkdir = Crea un directorio.")
        print("rmdir = Elimina un directorio.")
        print("mkfle = Crea un archivo.")
        print("mkuser = Crea un usuario.")
        print("rm = Elimina un archivo.")
        print("cd = Abrir un directorio.")
        print("cp = Copia un archivo.")
        print("pt = Pega un archivo.")
        print("ls = Muestra los directorios y archivos en los que estás.")
        print("exit = Salir.")
        print("clear = Limpia todo el texto.")
        print("refetch = Muestra información del sistema y hardware.")
        print("chuser = Cambiar de usuario.")
        print("logout = Cerrar sesión.")
        print("disa = \033[31m(¡No recomendado!)\033[0m Desactiva el sandboxing y permite interactuar con el sistema.")
        print("ensa = Activa el sandbox. \033[90m(Si lo desactivaste anteriormente)\033[0m")
        print("pkg --help = Mostrar los comandos para los paquetes.")
        print("exec = Ejecuta una app instalada.")
        print("edit = Editar un archivo.")
        print("devmode = Permite comandos especiales solo para desarrolladores.")

    elif comando == "devmode":
        dev = True
        print("Comandos para desarrolladores activados, escibe '-d' para ver más comandos.")

    elif comando == "-d":
        if dev == False:
            print("devmode no está activado.")
            continue
        else:
            print("\033[034mautojson\033[0m = Permite autogenerar archivos .json automaticos para facilitar la creación de aplicaciones.")

    elif comando == "pkg --help":
        print("pkg -list = Muestra la lista de paquetes para instalar")
        print("pkg -remove = Permite desinstalar una aplicación")

    elif comando == "autojson":
        if dev == False:
            print("devmode no está activado.")
            continue
        else:
            nombre_inicial = input("1. Introduce el nombre del proyecto ('q' para cancelar): ")
            version = input("2. Introduce la versión del proyecto:  ")
            archivo_principal = input("3. Introduce el archivo principal (nombre exacto y con formato): ")

            datos_json = {
                "name": nombre_inicial,
                "version": version,
                "main_file": archivo_principal
            }
        
        nombre_archivo = "info.json"
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos_json, archivo, indent=2, ensure_ascii=False)
            print(f"\n¡Éxito! El archivo '{nombre_archivo}' ha sido generado automáticamente.")

    elif comando == "cp":
        cp()

    elif comando == "pt":
        pt()

    elif comando == "test":
        print(userscanning(usuarioscarpeta))

    elif comando == "ls":
        print(os.listdir())
    elif comando == "mkdir":
        carpeta_nueva = input("Nombre del directorio: ")
        os.mkdir(carpeta_nueva)
    elif comando == "rmdir":
        try:
            remover_carpeta = input("Carpeta a remover: ")
            os.rmdir(remover_carpeta)
            print(f"Carpeta '{remover_carpeta}' eliminada con éxito.")
        except FileNotFoundError:
            print(f"\033[31mNo se encontró {remover_carpeta}.\033[0m")
        except OSError:
            print("El directorio no está vacío.")

    elif comando == "cd":
        try:
            ir_a = input("Ir a directorio: ")
            os.chdir (ir_a)
            print(f"Ahora estás en: ({os.getcwd()})")
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

    elif comando == "mkuser":
        mknewuser = input("Nombre del usuario nuevo (Usa 'q' para cancelar): ")
        users.append(mknewuser)
        make_folder_user = os.path.join(usuarioscarpeta, mknewuser)
        package_user_folder = os.path.join(make_folder_user, "packages")
        personalthings = input("¿Deseas integrar carpetas de paquetes para el usuario? (si / no) ").lower()
        if personalthings == "si":
            os.makedirs(package_user_folder, exist_ok=True)
        elif personalthings == "no":
            os.makedirs(make_folder_user, exist_ok=True)
        newuserfrommk == mknewuser

    elif comando == "logout":
        passtologout = True
        commandlogout = True
        print("Sesión cerrada (Usa login para volver, exit para salir.)")
                        
        while True:
            comandologout = input("> ")
            if comandologout == "login":
                print(userscanning(usuarioscarpeta))
                chooseuserlog = input("¿A que usuario quieres entrar? (Usa 'G' para entrar como invitado) ")
                
                if chooseuserlog in users:
                    working = True
                    passtologout = False
                    print(f"Sesión iniciada como {chooseuserlog}") 
                    break                    
                elif chooseuserlog.upper() == "G":
                    working = True
                    passtologout = False
                    print("Sesión iniciada como Invitado.")
                    break                    
                else:
                    print("Ese usuario no existe. Usa G para entrar como invitado.")
                    
            elif comandologout == "exit":
                print("Cerrando WintPy")
                working = False
                break

        if passtologout == True:
            working = False
    
    elif comando == "rm":
        try:
            remover = input("Archivo a remover: ")
            os.remove(remover)

        except FileNotFoundError:
            print(f"El archivo o carpeta '{remover}' no existe.")
        
        except (IsADirectoryError, PermissionError):
            print(f"'{remover}' es un directorio. Para borrar carpetas completas usa 'rmdir'.")
        
        except Exception as e:
            print(f"No se pudo eliminar: {e}")
            
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

    elif comando == "pkg -list":
        try:
            paquetes_disponibles = obtener_lista_paquetes()

            elegido = menu(paquetes_disponibles)

            print(obtener_lista_paquetes)

            if elegido:
                descargar_paquete(elegido)

        except Exception as e:
            print(""f"❌ Error en el gestor de paquetes: {e}")

    elif comando in ("run", "exec") or comando.startswith("run ") or comando.startswith("exec "):
        try:
            partes_consola = comando.strip().split()

            if len(partes_consola) < 2:
                app_elegida = input("¿Qué aplicación deseas ejecutar?: ").strip()
            else:
                app_elegida = partes_consola[1].strip()
            if app_elegida == "innovator":
                de = "Innovator DE"
            if not app_elegida:
                print("No introduciste ningún nombre.")
            else:
                ruta_carpeta = os.path.join("packages", app_elegida)
                archivo_py = f"{app_elegida}.py"
                ruta_ejecutable = os.path.join(ruta_carpeta, archivo_py)
                
                if os.path.exists(ruta_ejecutable):
                    # 1. PASAR EL FILTRO DE REQUISITOS ANTES DE ARRANCAR
                    if chequear_reqs(ruta_carpeta):
                        print(f"Lanzando {app_elegida}...\n")
                        subprocess.run([sys.executable, ruta_ejecutable])
                        print(f"\nVolviendo a WintPy.")
                    else:
                        print(f"❌ Lanzamiento cancelado por falta de dependencias.")
                else:
                    print(f"❌ Error: No se encontró '{archivo_py}' en 'packages/{app_elegida}/'")

        except Exception as e:
            print(f"❌ Error al ejecutar la app: {e}")

    elif comando == "mkfle":
        mkfle = input("Nombre del archivo y formato (No poner formato para un archivo simple): ")
        try:
            with open(mkfle, "x") as archivo:
                pass
            print("Archivo creado.")      
        except FileExistsError:
            print("[Error] Ese archivo ya existe en esta carpeta.")

    elif comando == "pkg -remove":
        try:
            ruta_packages = "packages"
            
            apps_instaladas = [
                f for f in os.listdir(ruta_packages) 
                if os.path.isdir(os.path.join(ruta_packages, f)) and not f.startswith("__")
            ]
        
            if len(apps_instaladas) == 0:
                print("No hay apps instaladas en el sistema.")
            else:
  
                print(f"\nApps instaladas ({len(apps_instaladas)}):")
                print("-" * 30)
                for app in apps_instaladas:
                    print(f" - {app}")
                print("-" * 30)
        
                uninstall = input("¿Qué app quieres desinstalar? (pon Q para cancelar): ").strip()
                ruta_a_borrar = os.path.join(ruta_packages, uninstall)
        
                if os.path.exists(ruta_a_borrar):
                    shutil.rmtree(ruta_a_borrar)
                    print(f"La aplicación '{uninstall}' se desinstaló correctamente.")
                    
                elif uninstall == "Q":
                    print("Operación cancelada.")
                    continue

                else:
                    print(f"No se encontró '{uninstall}' en el sistema.")
            
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

    elif comando == "edit":
        archivo_elegido = input("Introduce el nombre completo del archivo con su extensión: ")
        if os.path.exists(archivo_elegido):
            opcion = input("¿Quieres (A)ñadir texto al final o (S)obrescribirlo por completo? A / S: ")
        if opcion == "r":
            modo = "r"
            with open(archivo_elegido, "r", encoding="utf-8") as archivo:
                print(archivo.read())
                print("───────────────────────────────────────────\n")
            print("El archivo que introduciste no existe. \033[33m(Crea uno con mkfle)\033[0m")
            continue
        print("───────────────────────────────────────────\n")
        print("PyEditor 1.0.0")        
        print("\nEscribe el contenido (Escribe 'FIN' en una línea sola para terminar):")
        lineas = []
        while True:
            linea = input()
            if linea.upper() == "FIN":
                break
            lineas.append(linea + "\n")
            with open(archivo_elegido, modo, encoding="utf-8") as archivo:
                archivo.writelines(lineas)

        print(f"\n¡Listo! El archivo '{archivo_elegido}' ha sido actualizado.")



    elif comando == "refetch":
        segundos_totales = int(time.time() - tiempo_en_iniciar)
        minutos = segundos_totales // 60
        segundos = segundos_totales % 60
        if minutos > 0:
            texto_uptime = f"{minutos} min, {segundos} seg"
        else:
            texto_uptime = f"{segundos} seg"
            
        info = [
            "\033[34mWint\033[33mPy\033[0m OS 1.0.4 Main",
            "-------------------------",
            f"SO Base: {platform.system()}",
            f"Nombre del usuario: {socket.gethostname()}",
            f"Uptime: {texto_uptime}",
            f"Usuario: {user1name}",
            f"DE: {de}",
            "\033[32mHola!\033[0m"
        ]
        
        lineas_logo = wintpy_logo.strip().split('\n')
        
        for i, linea in enumerate(lineas_logo):
            texto_info = info[i] if i < len(info) else ""
            
            print(f"{linea.ljust(40)}   {texto_info}")
            
    else:
        print("Comando desconocido")
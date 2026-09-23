import os

def mostrar_intro():
    ancho_terminal = os.get_terminal_size().columns

    ANCHO_MAXIMO = 90
    ancho_diseno = min(ANCHO_MAXIMO, ancho_terminal)

    ancho_contenido = ancho_diseno - 2

    lineas_texto = [
        "",
        "CodePy 1.0",
        "El editor de texto hecho 100% en Python",
        "",
        "Hecho por Wyberdev",
        "",
        "  > escriba :new para crear un nuevo archivo",
        "  > escriba :open para abrir un archivo",
        "  > escriba :exit para salir",
        ""
    ]

    bloque_interfaz = []
    bloque_interfaz.append("=" * ancho_diseno)
    
    for linea in lineas_texto:
        bloque_interfaz.append(f"|{linea.center(ancho_contenido)}|")
        
    bloque_interfaz.append("=" * ancho_diseno)

    for linea in bloque_interfaz:
        print(linea.center(ancho_terminal))

mostrar_intro()
working = True
while working == True:
    introinput = input("").lower()
    match introinput:
        case ":new":
            newfilename = input("Nombre del archivo (Formato incluido): ")
            try:
                with open(newfilename, "x") as newfilecreate:
                    pass
            except FileExistsError:
                print("El archivo ya existe.")
    
        case ":open":
            openfilename = input("Archivo a abrir: ")
            try:
                with open(openfilename, "r", encoding="utf-8") as f:
                    lineas = f.readlines()                
                os.system('cls' if os.name == 'nt' else 'clear')
                editing = True
                working = False
                while editing == True:
                    print("\033[90mCtrl + O para guardar el archivo, Ctrl + E para salir\033[0m")
                
                for numero, line in enumerate(lineas, start=1):
                    print(f"{str(numero).rjust(3)}~ {line.rstrip()}")
                write = input("> ")

            except FileNotFoundError:
                print("El archivo no existe.")
        
        case ":exit":
            working = False

        case _:
            print("Comando desconocido.")
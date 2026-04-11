class Display:
    def __init__(self, robot):
        self._robot = robot

    
    def main_menu(self):
        print("Menú Principal")
        print("1. Ejecutar rutina.")
        print("2. Añadir rutina.")
        print("3. Gestionar Herramientas.")
    
    def options(self):
        opt = input("Elija una opción.")
        self.main_menu()
        match opt:
            case "1": pass
            case "2": pass
            case "3": pass
            case _: print("opción no válida")
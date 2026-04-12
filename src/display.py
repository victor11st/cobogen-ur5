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
            case "1": 
                print("Rutinas disponibles.")
                num_routines = {}
                for number, routine in enumerate(self._robot.available_routines):
                    num_routines[number] = routine
                    print(f"{number}. {routine}.")
                selected_routine = input("Seleccione una rutina:")
                self._robot.execute_routine(selected_routine)
                
            case "2": self.teach_mode()
            case "3": pass
            case _: print("opción no válida")


    def teach_mode(self):
        print("Añadir nueva rutina")
        name_new_routine = input("Nombre de la nueva rutina (no se admiten espacios):")
        list_points = []
        while True:
            opc = input("Pulse 1 para añadir un punto o pulse 2 para terminar de crear rutina o pulse 3 para salir.")
            match opc:
                case "1": 
                    name_point = print("Escriba el nombre del punto o enter para omitir: ")
                    if input == "":
                        name_point = None
                    new_point = self._robot.add_point(name_point)
                    list_points.append()
                    print("Punto guardado correctment.")
                case "2":
                    self._robot.add_routine(new_point)

                case "3": break
                case _: print("Opción no vaálida")

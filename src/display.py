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
                    name_routine = input("Esriba el nombre de la nueva rutina")
                    new_point = self.request_point_info()
                    name_point = new_point["name"]
                    coord = new_point["coord"]
                    config = new_point["config"]
                    
                    if name_point in self._robot.available_points:
                        sobrescribir = input("Punto existente. ¿Desea sobreescribirlo? (S/N): ")
                        if sobrescribir == "S":
                            self._robot.add_point(name_point, coord)
                        else:
                            print("Acción cancelada")
                            continue
                    else:
                        self._robot.add_point(name_point, coord)
                    
                    self._robot.add_routine(name_routine, config)
                    print("Punto añadido a rutina correctamente.")
                    
                case "2":
                    self._robot.add_routine(new_point)

                case "3": break
                case _: print("Opción no vaálida")


    def request_point_info(self):
        position = self._robot.tcppose[:3]
        orientation = self._robot.tcppose[3:]

        name_point = input("Escriba el nombre del punto o pulse enter para omitir (no se admiten espacios).")
        type_move_point = input("El movimiento al punto sera de tipo Joint(j) o de tipo Linear (L):")
        speed = input("Velocidad a la que se llegará al punto. Por defecto  :")
        acceleration = input("Aceleracion a la que se llegará al punto. Por defecto  :")

        if name_point == "":
            name_point = None

        new_point_pose = {
            "position":position,
            "orientation":orientation 
        }
    
        new_point_config = {
             "name":name_point,
             "type":type_move_point,
             "speed":speed,
             "acceleration":acceleration
        }

        new_point = {
            "name":name_point,
            "coord":new_point_pose,
            "config":new_point_config
        }


        return new_point
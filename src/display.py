class Display:
    def __init__(self, robot):
        self._robot = robot

    
    def main_menu(self):
        print("Menú Principal")
        print("1. Ejecutar rutina.")
        print("2. Añadir rutina.")
        print("3. Gestionar Herramientas.")

        
    def _teach_mode_menu(self):
        print("1. Añadir punto.")
        print("2. Terminar.")

    def _gestor_tool_menu(self):
        print("1. Ver todas las herramientas.")
        print("2. Calibrar TCP de herramienta.")
        print("3. Añadir nueva herramienta.")
        print("4. Salir.")

    def options(self):
        opt = input("Elija una opción.")
        self.main_menu()
        match opt:
            case "1": 
                self._execute_routine()
            case "2": 
                self.teach_mode()
            case "3":
                self._gestor_tool()
            case _: 
                print("opción no válida")



    def _gestor_tool(self):
        print("\n opciones:")
        while True:
            self._gestor_menu()
            opc = input("Selecciones la opcíon que desee")
            match opc:
                case "1":
                    self._list_tools()
                case "2":
                    self.add_tool()
                case "3":
                    self._calibrate_tool()
                case _:
                    break

    def _list_tools(self):
        print("Herramientas")
        for num, tool in enumerate(self._robot.tools, 1):
            if tool == self._robot.activate_tool:
                print(f"{num}. {tool} <- Herramienta activa")
            else:
                print(f"{tool}")


    def _add_tool(self):
        print("AÑADIR HERRAMIENTA")
        name = input("Nombre de la herramienta: ")
        x = input("Indique cordenada desde la brida en eje x en milimetros: ")
        y = input("Indique cordenada desde la brida en eje y en milimetros: ")
        z = input("Indique cordenada desde la brida en eje z en milimetros: ")
        rx = input("Grados en de inclunación en el eje x: ")
        ry = input("Grados en de inclunación en el eje y: ")
        rz = input("Grados en de inclunación en el eje z: ")
        position = [x, y, z]
        orientation = [rx, ry, rz]
        tcp_new_tool = position + orientation

        self._robto.add_tool(tcp_new_tool)
        


    def _caliblate_tool(self):
        print()
        self._list_tools()
        tool = input("Elija la herramienta que desee calibrar: ")
        if tool <= len(self._robot.tools):
            print(f"Calibrando herramienta {self._robot.tools[tool - 1]}")
            self._robot.calibrate(tool - 1)
        else:
            print("Herramienta no encontrada")

            

    def _execute_routine(self) -> None:
        print("Rutinas disponibles.")
        for number, routine in enumerate(self._robot.available_routines, 1):
            print(f"{number}. {routine}.")
        selected_routine = input("Seleccione una rutina:")
        self._robot.execute_routine(selected_routine)


    def _teach_mode(self) -> None:
        """
        The options for add routine
        """
        print("Añadir nueva rutina")
        routine_name = input("Esriba el nombre de la nueva rutina")
        while True:
            self._teach_mode_menu()  
            opc = input("Seleccione una opción.")          
            match opc:
                case "1":
                    self._handle_add_point_to_routine(routine_name)
                case "2": 
                    break
                case _: 
                    print("Opción no vaálida")

    def _handle_add_point_to_routine(self, routine_name:str) -> None:
        """
        Add new points for new routine
        """
        new_point = self._request_point_info()

        name_point = new_point["name"]
        coord = new_point["coord"]
        config = new_point["config"]
        
        if name_point in self._robot.available_points:
            sobrescribir = input("Punto existente. ¿Desea sobreescribirlo? (S/N): ")
            if sobrescribir == "S":
                self._robot.add_point(name_point, coord)
            else:
                print("Acción cancelada")
                return
        else:
            self._robot.add_point(name_point, coord)
        
        self._robot.add_routine(routine_name, config)
        print("Punto añadido a rutina correctamente.")


    def _request_point_info(self) -> dict[str:str|dict[str:str|float]]:
        """
        Request all information of the new point at the user.
        """
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
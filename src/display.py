import ur5   
import os

class Display:
    def __init__(self, robot):
        self._robot = robot

    @staticmethod
    def _clean_display():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def _main_menu():
        print("MENÚ PRINCIPAL")
        print("1. Modo IA(CoboGen).")
        print("2. Ejecutar secuencia manual.")
        print("3. Mapear posición.")
        print("4. Programar microrutina.")
        print("5. Configuración del cobot (hardware).")
        print("6. Gestor de memoria (Limpieza)")
        print("7. Salir.")


    def options(self):
        while True:
            Display._clean_display()
            Display._main_menu()
            opt = input("Elija una optión.")
            Display._clean_display()
            match opt:
                case "1": 
                    self._execute_routine() #modo ia
                case "2": 
                    self._execute_routine()  # pruebas
                case "3":
                    self._handle_add_point_to_routine()
                case "4":
                    self._teach_mode()
                case "5":
                    self._config_hardware()
                case "6":
                    self._memory_manager()
                case "7":
                    break
                case _: 
                    print("optión no válida")
            Display._clean_display()



    @staticmethod
    def _config_hardware_menu():
        print("\n CONFIGUURACIÓN DEL COBOT")
        print("1. Ver y seleccionar herramienta activa.")
        print("2. Calibrar herramienta existente.")
        print("3. Añadir nueva herramienta.")
        print("4. Eliminar herramienta.")
        print("5. Volver al menú principal.")


            
    @staticmethod
    def _get_tcp_menu():
        x = Display._get_float_input(messege="Indique cordenada desde la brida en eje x en milimetros: ")
        y = Display._get_float_input(messege="Indique cordenada desde la brida en eje y en milimetros: ")
        z = Display._get_float_input(messege="Indique cordenada desde la brida en eje z en milimetros: ")
        rx = Display._get_degree(messege="Grados de inclunación en el eje x: ")
        ry = Display._get_degree(messege="Grados de inclunación en el eje y: ")
        rz = Display._get_degree("Grados de inclunación en el eje z: ")
        return [x, y, z, rx, ry, rz]




    @staticmethod
    def _memory_manager_menu():
        print("\n GESTOR DE MEMORIA")
        print("1. Ver lista de puntos mapeados.")
        print("2. Ver lista de micro-rutinas.")
        print("3. Eliminar punto.")
        print("4. Eliminar una micro-rutina.")
        print("5. Volver al menú principal.")


    @staticmethod
    def _teach_mode_menu():
        print("\n CREACIÓN DE PUNTO")
        print("1. Capturar coordenadas actuales (FreeDrive)")
        print("2. Cancelar y volver")


    @staticmethod
    def _overwrite_point_menu():
        print("Punto ya existe.")
        print("1. Sobreescribir punto.")
        print("2. Volver a intentar definir punto.")
        print("3. Cancelar operación.")


    @staticmethod
    def _gestor_routine_opttion_menu(routine_selected):
        print(f"Rutina seleccionada: {routine_selected}")
        print("1. Modificar rutina.")
        print("2. Eliminar rutina.")
        print("3. Cancelar operación.")




    @staticmethod
    def _request_info_point_menu():
        while True:
            name_point = input("Escriba el nombre del punto: ")
            if name_point.strip() == "":
                input("Nombre no valido.")
                Display._clean_display
            else:
                break

        while True:
            Display._clean_display()
            print("Tipo de movimiento:")
            print("1. Linear.")
            print("2. Joint.")
            opt = input("Seleccione una optión.")
            match opt:
                case "1": 
                    type_move = "linear" 
                    break
                case "2": 
                    type_move = "joint"
                    break
                case _: input("optión no valida")
        Display._clean_display()
        speed = Display._get_float_input(messege="Velocidad (optional: 0.5 por defecto): ", default=0.5)
        acceleration = Display._get_float_input(messege="Aceleración (optional: 1.0 por defecto): ", default=1.0)
        
        config_new_point = {
            "name":name_point,
            "type":type_move,
            "speed":speed,
            "acceleration":acceleration
        }
    
        return config_new_point

    
    @staticmethod
    def _get_float_input(messege:str, default:float = None) -> float:
        while True:
            input_messege = input(messege).strip()

            if input_messege == "":
                return default
            
            try:
                Display._clean_display()
                return float(input_messege)
            
            except ValueError:
                input("Error: El valor debe ser numerico.")
                Display._clean_display()

    @staticmethod
    def _get_degree(messege):
        while True:
            input_degree = input(messege).strip()
            try:
                degree = float(input_degree)
                if abs(degree) > 360:
                    print("Error: Los grados deben estar entre -360 y 360.")
                    continue
                return degree
            except ValueError:
                print("Error: El valor debe ser numerico.")

    @staticmethod
    def _display_generic_list(items: list, empty_msg: str, header_msg: str, active_item=None) -> dict:
        """Solo imprime una lista de datos y devuelve el diccionario base."""
        options_dict = {}
        
        if not items:
            input(f"\n{empty_msg}")
            return options_dict
            
        print(f"\n{header_msg}")
        for num, item in enumerate(items, 1):
            if active_item and item == active_item:
                print(f"{num}. {item} <- Herramienta activa")
            else:
                print(f"{num}. {item}")
            options_dict[str(num)] = item
        return options_dict

    @staticmethod
    def _add_exit_option(options_dict: dict) -> dict:
        """Añade la opción de salir al final de un diccionario y la imprime por pantalla."""
        exit_num = len(options_dict) + 1
        options_dict[str(exit_num)] = "salir"
        print(f"{exit_num}. Salir.")
        return options_dict


    def _config_hardware(self):
        print("\n optiones:")
        while True:
            Display._config_hardware_menu()
            opt = input("Selecciones la optíon que desee")
            Display._clean_display()     
            match opt:
                case "1":self._show_and_select_tool()
                case "2":self._calibrate_tool()
                case "3":self._add_tool()
                case "4":self._delete_tool()
                case "5":break
                case _: input("optión no válida.")


    def _list_points(self) -> dict:
        Display._clean_display()
        return Display._display_generic_list(
            items=self._robot.available_points,
            empty_msg="No hay puntos registrados.",
            header_msg="Puntos registrados:"
        )


    def _list_tools(self) -> dict:
        Display._clean_display()
        return Display._display_generic_list(
            items=self._robot.tools,
            empty_msg="No hay herramientas definidas.",
            header_msg="Herramientas definidas:",
            active_item=self._robot.active_tool
        )

    def _lists_routines(self) -> dict:
        Display._clean_display()
        return Display._display_generic_list(
            items=self._robot.available_routines,
            empty_msg="No hay rutinas registradas.",
            header_msg="Rutinas registradas:"
        )




    def _memory_manager(self):
        while True:
            self._clean_display()

            self._memory_manager_menu()
            opt = input("Seleccione una optión: ")
            match opt:
                case "1": 
                    self._list_points()
                    input()
                case "2": 
                    self._lists_routines()
                case "3": self._remove_point()
                case "4": self._remove_routines()
                case "5": break
                case _: input("optión no valida.")
            self._clean_display()
    




    def _remove_routines(self):
        while True:
            options = self._lists_routines()
            if options:
                options = self._add_exit_option(options)
                opt = input("Seleccione una optión")
                if opt in options:
                    if options[opt] == "salir":
                        break
                    name_routine = options[opt]
                    point_delete = self._robot.delete_routine(name_routine)
                    print(f"La rutina {point_delete} fue eliminada correctamente.")
                    break
                else:
                    print("optión no válida") 
            else:
                break


    def _remove_point(self):
        while True:
            self._clean_display()
            options = self._list_points()
            if options:
                options = self._add_exit_option(options)
                opt = input("Seleccione una optión: ")
                if opt in options:
                    if options[opt] == "salir":
                        break
                    name_point = options[opt]
                    point_delete = self._robot.delete_point(name_point)
                    print(f" El punto {point_delete} fue eliminado correctamente.")
                    break
                else:
                    print("optión no válida")
            else:
                break
        




    def _show_and_select_tool(self):
        while True:

            print("Cambiar herramienta.")
            tools = self._list_tools()
            if not tools:
                print("No hay herramientas definidas.")
            
            else:
                opt = input("seleccione: una optión:")

                if opt in tools:
                    if tools[opt] == "salir":
                        return
                    else:
                        name_tool = tools[opt]
                        self._robot.change_active_tool(name_tool)
                        print(f"{name_tool} activa.")
                        break
                else:
                    input("optión no valida.")

        


    def _delete_tool(self):
        while True:
            tools = self._list_tools()
            opt = input("seleccione: una optión:")
            name_tool = tools[opt]
            if not tools:
                print("No hay herramientas definidas.")
            elif opt in tools:
                if tools[opt] == "salir":
                    break
                else:
                    tool = self._robot.delete_tool(name_tool)
                    input(f"{tool} fue eliminado correctamente.")
            else:
                print("Herramienta no existe")
         





    def _add_tool(self):
        print("AÑADIR HERRAMIENTA")
        name = input("Nombre de la herramienta: ")
        tcp_new_tool = Display._get_tcp_menu()
        self._robot.add_tool(name, tcp_new_tool)
        Display._clean_display()


    def _calibrate_tool(self):
        self._show_and_select_tool()
        self._list_tools()
        tool = input("Elija la herramienta que desee calibrar: ")
        if tool <= len(self._robot.tools):
            print(f"Calibrando herramienta {self._robot.tools[tool - 1]}")
            self._add_tool()
        else:
            print("Herramienta no encontrada")


    def _execute_routine(self):
        while True:
            print("RUTINAS.")
            routines = self._lists_routines() 
            if not routines:
                input("No hay rutinas definidas")
                break
            opt = input("Seleccione rutina:")
            if opt in routines:
                if routines[opt] == "salir":
                    break
                name_routine = routines[opt]
                self._robot.execute_routine(name_routine)
            else:
                input("No existe rutina")

            




    def _teach_mode(self) -> None:
        """
        The options for add routine
        """
        print("Añadir nueva rutina")
        routine_name = input("Esriba el nombre de la nueva rutina: ")
        if routine_name not in self._robot.available_routines:
            while True:
                Display._teach_mode_menu()  
                opt = input("Seleccione una optión.")          
                match opt:
                    case "1":
                        Display._clean_display()
                        self._create_routines()
                    case "2": 
                        break
                    case _: 
                        print("optión no vaálida")
        else:
            input("Rutina ya existe, si desea modificarlo, dirigase a gestionar rutinas en el menu de optiones")


    def _create_routine(self):
        routine = []
        name_routine = input("Nombre de la rutina.")
        while True:
            print("Crear rutina")
            options = self._list_points()
            options = self._add_exit_option()
            opt = input("ELija el sigiente punto para crear la rutina:")
            if options == "salir":
                routine = self._routine_and_config()
                self._robot.add_routine(name_routine, routine)
            else:
                routine.append(options[opt])

            



    def _handle_add_point_to_routine(self:str) -> None: #revisar
        """
        Add new points for new routine
        """
        while True:
            Display._clean_display()
            new_point = self._get_point_info()
            name_point = new_point["name"]
            if name_point in self._robot.available_points:
                self._clean_display()
                Display._overwrite_point_menu()
                opt = input("Seleccione una optión: ")
                match opt:
                    case "1":
                        self,self._confirmation_add_point(new_point)
                        break
                    case "2":
                        continue
                    case "3":
                        break
                    case _:
                        input(print("optión no valida."))
                        Display._clean_display()
            else:
                self._confirmation_add_point(new_point)
                break
    
    def _confirmation_add_point(self,new_point):
        name_point = new_point["name"]
        coord = new_point["coord"]
        config = new_point["config"]

        position = coord["position"]
        orientation = coord["orientation"]
   
        type_move = config["type"] 
        speed = config["speed"]
        acceleration = config["acceleration"] 

        while True:
            print("PUNTO CONFIGURADO")
            print(f"Nombre del punto: {name_point}   Tipo de movimiento: {type_move}")
            print(f"Posicíon: {position}    Orientación: {orientation}")
            print(f"Velocidad: {speed}   Aceleración: {acceleration}")
            opt = input("¿Desea añadir el punto? (s/n): ")
            self._clean_display()
            match opt:
                case "s":
                    self._robot.add_point(coord)
                    # self._robot.add_routine(routine_name, config)
                    input("punto añadido correctamente")
                    break
                case "n":
                    input("Punto no añadido.")
                    break
                case _:
                    input("Opción no valida")




    def _get_point_info(self) -> dict[str:str|dict[str:str|float]]:
        """
        Request all information of the new point at the user.
        """
        position = self._robot.tcp_pose[:3]
        orientation = self._robot.tcp_pose[3:]

        config_new_point = Display._request_info_point_menu()            
        name_point = config_new_point["name"]
        type_move = config_new_point["type"]
        speed = config_new_point["speed"]
        acceleration = config_new_point["acceleration"]


        new_point_pose = {
            "name":name_point,
            "position":position,
            "orientation":orientation 
        }
    
        new_point_config = {
            "name":name_point,
             "type":type_move,
             "speed":speed,
             "acceleration":acceleration
        }

        new_point = {
            "name":name_point,
            "coord":new_point_pose,
            "config":new_point_config
        }
        return new_point
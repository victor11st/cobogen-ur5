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


    def run(self):
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
                    self._create_point()
                case "4":
                    self._create_routine()
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
    def _add_routine_menu():
        print("AÑADIR RUTINA")
        print("1. Añadir punto a la secuencia.")
        print("2. Eliminar ultimo punto añadido.")
        print("3. Guardar rutina y salir.")
        print("4. Cancelar operación.")




    
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
        while True:
            Display._config_hardware_menu()
            opt = input("Selecciones la opción que desee: ")
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
                    input()
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
                    if options[opt] == "home":
                        print("ERROR: Home no puede ser eliminado, si quiere modificarlo, dirigase a mapear posicion para sobreescribirlo.")
                        continue
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
            options = self._list_tools()
            options = self._add_exit_option(options)          

            opt = input("seleccione: una optión:")

            if opt in options:
                if options[opt] == "salir":
                    break
                else:
                    name_tool = options[opt]
                    self._robot.change_active_tool(name_tool)
                    print(f"{name_tool} activa.")
                    break
            else:
                input("optión no valida.")

        


    def _delete_tool(self):
        while True:

            Display._clean_display()
            print("Eliminar herramienta.")
            options = self._list_tools()
            options = self._add_exit_option(options)          

            opt = input("seleccione: una optión:")

            if opt in options:
                if options[opt] == "salir":
                    break
                elif options[opt] in self._robot.active_tool:
                    print("Herramienta activa no puede ser eliminada.")
                else:
                    name_tool = options[opt]
                    self._robot.delete_tool(name_tool)
                    print(f"{name_tool} activa.")
                    break
            else:
                input("optión no valida.")

         

    def _add_tool(self):
        print("AÑADIR HERRAMIENTA")
        name = input("Nombre de la herramienta: ")
        tcp_new_tool = Display._get_tcp_menu()
        mass = Display._get_float_input(messege="peso de la herramienta")
        self._robot.add_tool(name, tcp_new_tool, mass)
        Display._clean_display()


    def _calibrate_tool(self):
        print("CALIBRAR HERRAMIENTA")
        options = self._list_tools()
        if not options: return
        options = self._add_exit_option(options)
        
        option = input("\nElija la herramienta que desee calibrar: ").strip()
        if option in options:
            if options[option] == "salir": return
            print(f"Calibrando herramienta: {options[option]}")
            self._add_tool() # Asumes that add_tool overwrites the existing one
        else:
            input("Opción no encontrada.")      

    def _execute_routine(self):
        while True:
            print("RUTINAS.")
            options = self._lists_routines() 
            options = self._add_exit_option(options)
            opt = input("Seleccione rutina:")
            if opt in options:
                if options[opt] == "salir":
                    break
                name_routine = options[opt]
                self._robot.execute_routine(name_routine)
            else:
                input("No existe rutina")

            







    @staticmethod
    def _add_point_menu():
        print("¿Desea añadir un punto?.")
        print("1. Para guardar punto.")
        print("2. Finalizar.")


    def _create_point(self):
        while True:
            self._clean_display()
            self._add_point_menu()
            opt = input("Seleccione una opción: ")
            match opt:
                case "1":
                    self._add_point()
                case "2":
                    break
                case _: 
                    input("Opción no valida")





    def _add_point(self):
        self._clean_display()
        name_point = input("Nombre del punto: ")
        if name_point in self._robot.available_points:
            while True:
                self._clean_display()
                self._overwrite_point_menu()
                opt = input("Seleccione una opción")
                match opt:
                    case "1":
                        self._robot.add_point(name_point)
                        break
                    case "2":
                        break
                    case _: print("Opción no válida.")
        else:
            self._robot.add_point(name_point)



    def _create_routine(self) -> None:
        """
        The options for add routine
        """
        name_routine = input("Esriba el nombre de la nueva rutina: ")
        if name_routine not in self._robot.available_routines:
            points_config = []
            while True:
                Display._clean_display()
                Display._add_routine_menu()  
                opt = input("Seleccione una optión.")
                match opt:
                    case "1":
                        config_point = self._add_point_to_routine()
                        points_config.append(config_point)
                    case "2":
                        points_config.pop()
                    case "3":
                        self._save_routine(points_config, name_routine)
                        break
                    case "4":
                        break
                    case _: 
                        input("Opción no válida.")



    def _save_routine(self, points_config, name_routine):
        self._robot.add_routine(points_config, name_routine)
        print(f"La rutina {name_routine} fue añadida correctamente.")


    def _add_point_to_routine(self):

        Display._clean_display()
        options = self._list_points()
        options = self._add_exit_option(options)
        opt = input("Seleccione una opción:")
        if opt in options:
            if options[opt] == "salir":
                return
            else:
                name_point = options[opt]
                config_point = self._request_info_point(name_point)
                if self._confirmation_add_point(config_point):
                    return config_point
        else:
            input("Opción no valida")
        return None
        
                



    @staticmethod
    def _confirmation_add_point(config_point:dict):

        name_point = config_point["name"]
        type_move = config_point["type"] 
        speed = config_point["speed"]
        acceleration = config_point["acceleration"] 

        while True:
            print("MOVIMIENTO CONFIGURADO")
            print(f"Nombre del punto: {name_point}   Tipo de movimiento: {type_move}")
            print(f"Velocidad: {speed}   Aceleración: {acceleration}")
            opt = input("¿Desea añadir el punto? (s/n): ")
            Display._clean_display()
            match opt:
                case "s":
                    input("punto añadido correctamente")
                    return True
                case "n":
                    input("Punto no añadido.")
                    return False
                case _:
                    input("Opción no valida")




    @staticmethod
    def _request_info_point(name_point):

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
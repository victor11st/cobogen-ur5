import rtde_receive
import rtde_control
import math
import json

class UR5():
    "Robot UR5"
    _JOINT_LIMIT_DEG = 355

    def __init__(self, ip: str, tools: dict[str:tuple[int]], workplace: list[float], home: tuple[float], path_json: str):
        tools = UR5._validate_tools(tools)
        self._home = UR5._validate_home(home)
        

        # Interfaces
        self._receptor = rtde_receive.RTDEReceiveInterface(ip)
        self._controlador = rtde_control.RTDEControlInterface(ip)

        full_data = UR5.laod_from_json(path_json)
        self._workplace = workplace
        self._tools = tools
        self._active_tool = None
        self._estate = None
        self._tcp = None
        self._points = full_data.get("points", {})
        self._routines = full_data.get("routines", {})
        self._auto_point_counter = 0 # Adapter for JSON

#-----------| GETTERS |-------------------
    @property
    def home(self):
        return self._home

    @property
    def available_routines(self):
        return list(self._routines.keys())
    
    @property
    def available_points(self):
        return list(self._points.keys())


    @property
    def active_tool(self):
        return self.active_tool
#-------------------------------------------

#----------| SETTERS |-----------------------
    @home.setter
    def home(self, new_home: str):
        self._home = UR5._validate_home(new_home)
#------------------------------------------

    @staticmethod
    def laod_from_json(json_path:str):
        try:
            with open(json_path, 'r') as f:
                full_data = json.load(f)
            return full_data
        except FileNotFoundError:
            print("Fichero no encontrado")
        except json.JSONDecodeError:
            print(f"Error: El archivo JSON tiene un formato incorrecot")


    @staticmethod
    def _validate_home(home: tuple[float]):
        for grades_motor in home:
            if abs(grades_motor) > UR5._JOINT_LIMIT_DEG:
                return None
        return UR5._deg_to_rad(home)


    @staticmethod
    def _validate_tools(tools: dict[str:tuple[int]]):
        for name, tcp in tools.intems():
            if len(tcp) != 6:
                tool_deleted = tools.pop(name)
                print(f"{tool_deleted} was ignored: Values incorrect.")        
        return tools

    @staticmethod
    def _deg_to_rad(values: tuple[float|int]) -> list[float]:
        return tuple(math.radians(d) for d in values)

    @staticmethod
    def _mm_to_m(value):
        return [mm/1000.0 for mm in value]

    def add_tool(self, tools: dict[str:tuple]):
        """
        Add news tools
        """
        tools = self._validate_tools(tools)
        if tools:
            for name, tcp in tools:
                self._tools[name] = tcp

    def delete_tool(self, name_tool):
        tool = self._tools.pop(name_tool)
        print(f"Se eliminó {tool} correctamente.")


    def change_active_tool(self, name_tool):
        """
        Change tool.
        """
        self.controlador.setTcp(self.herramientas[name_tool] )
        self.active_tool = name_tool

        print("The tool active is:", self.active_tool)
    


    def move_to_home(self):
        """
        Move the robot at the home position
        """
        self._controlador.moveJ(self._home)


    def execute_routine(self, name_routine:str) -> None:
        """
        Execute routine.
        """
        routine = self._routines[name_routine]
        points = self._points
        for target in routine:
            name = target["name"]
            type_mov = target.get("type", "joint")
            speed = target.get("speed", 0.5)
            acceleration = target.get("acceleration", 1.0)
            
            aux = points[name]

            point = aux["position"] + aux["orientation"]

            if type_mov == "joint":
                self._controlador.moveJ_IK(point, speed, acceleration)

            elif type_mov == "linear":
                self._controlador.moveL(point, speed, acceleration)
  
    def add_routine(self, new_points:list[dict], name_routine:str):
        self._routines[name_routine].append(new_points)

    def add_point(self, new_point:dict[str:list[float]], config_new_point:dict[str:str|float]) -> dict:
        position = new_point["position"]
        new_point = new_point["orientation"]

        name_point = config_new_point["name"]
        type_move_point = config_new_point["type"]
        speed = config_new_point["speed"]
        acceleration = config_new_point["acceleration"]

        coord_point = self._receptor.getActualPose()
        if name_point == None:
            name_point == f"point_{self._auto_point_counter}" #Generate auto name to point
        position = coord_point[:3]
        orientation = coord_point[3:]

        new_point = {
            "position":position,
            "orientation":orientation 
        }
    
        conf_new_point = {
             "name":name_point,
             "type":type_move_point,
             "speed":speed,
             "acceleration":acceleration
        }


        self._points[name_point] = new_point 
        return config_new_point
            
            


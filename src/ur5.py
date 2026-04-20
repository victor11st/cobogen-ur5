import rtde_receive
import rtde_control
import math
import json
import time
from functools import wraps


def reload_script(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self._controlador.isProgramRunning():
            print("Reconectando con el robot")
            self._controlador.reuploadScript()
            time.sleep(1)
        return func(self, *args, **kwargs)
    return wrapper



class UR5():
    "Robot UR5"
    _JOINT_LIMIT_DEG = 355

    def __init__(self, ip: str,home: tuple[float], workplace: list[float] = None, path_json: str = None, tools: dict[str:tuple[int]] = {}):
        self._home = UR5._validate_home(home)
        

        # Interfaces
        self._receptor = rtde_receive.RTDEReceiveInterface(ip)
        self._controlador = rtde_control.RTDEControlInterface(ip)

        #full_data = UR5.laod_from_json(path_json)
        full_data = {}
        self._workplace = workplace
        self._tools = tools
        self._active_tool = None
        self._estate = None
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
        return self._active_tool
    
    @property
    def tools(self):
        return self._tools
    
    @property
    def tcp_pose(self):
        return self._receptor.getActualTCPPose()
#-------------------------------------------

#----------| SETTERS |-----------------------
    @home.setter
    def home(self, new_home: str):
        self._home = UR5._validate_home(new_home)
#------------------------------------------


    @staticmethod
    def _load_from_json(self):
        pass

    @staticmethod
    def _validate_json(json_path:str):
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
    def _deg_to_rad(values: tuple[float|int]) -> list[float]:
        return tuple(math.radians(d) for d in values)

    @staticmethod
    def _mm_to_m(value):
        return [mm/1000.0 for mm in value]



    def delete_tool(self, name_tool):
        tool = self._tools.pop(name_tool)
        return tool
    def delete_routine(self, name_routine):
        routine = self._routines.pop(name_routine)
        return routine
    
    def delete_point(self, name_point):
        name_point = self._points.pop(name_point)
        return name_point

    def change_active_tool(self, name_tool):
        """
        Change tool.
        """
        self.controlador.setTcp(self.herramientas[name_tool] )
        self.active_tool = name_tool
    

    @reload_script
    def move_to_home(self):
        """
        Move the robot at the home position
        """  
        self._controlador.moveJ(self._home)

    @reload_script
    def execute_routine(self, name_routine:str) -> None:
        """
        Execute routine.
        """
        routine = self._routines[name_routine]
        points = self._points
        for target in routine:
            name = target["name"]
            type_mov = "joint"
            speed = target.get("speed", 0.5)
            acceleration = target.get("acceleration", 1.0)
            
            aux = points[name]

            point = aux["position"] + aux["orientation"]

            if speed == "": speed = 0.5
            if acceleration == "": acceleration = 1.0

            # if type_mov == "joint":
            self._controlador.moveJ_IK(point, speed, acceleration)
            print(point)
            print(speed)
            print(acceleration)
            print("en reoria se movio")
            # elif type_mov == "linear":
            #     self._controlador.moveL(point, speed, acceleration)
  

    def add_routine(self, name_routine, routine:dict) -> None:
        pass            

    def add_point(self, coord:dict) -> bool:
        name_point = coord["name"]
        position = coord["position"]
        orientation = coord["orientation"]

        self._points[name_point] = {
            "position":position,
            "orientation":orientation
        }


    def add_tool(self, name, tcp_new_tool) -> None:
        self._active_tool = name
        self._tools[name] = tcp_new_tool


    


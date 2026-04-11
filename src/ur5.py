import rtde_receive
import rtde_control
import math

class UR5():
    "Robot UR5"
    _JOINT_LIMIT_DEG = 355

    def __init__(self, ip: str, tools: dict[str:tuple[int]], workplace: list[float], home: tuple[float], sequence):
        tools = UR5._validate_tools(tools)
        self._home = UR5._validate_home(home)

        # Interfaces
        self._receptor = rtde_receive.RTDEReceiveInterface(ip)
        self._controlador = rtde_control.RTDEControlInterface(ip)

        self._workplace = workplace
        self._tools = tools
        self._active_tool = None
        self._estate = None
        self._tcp = None
        self._sequence = sequence


    @property
    def home(self):
        return self._home
    
    @home.setter
    def home(self, new_home: str):
        self._home = UR5._validate_home(new_home)

    @property
    def active_tool(self):
        return self.active_tool


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
        tools = self._validate_tools(tools)
        if tools:
            for name, tcp in tools:
                self._tools[name] = tcp


    def change_active_tool(self, name_tool):
        self.controlador.setTcp(self.herramientas[name_tool] )
        self.active_tool = name_tool

        print("The tool active is:", self.active_tool)
    


    def move_to_home(self):
        self._controlador.moveJ(self._home)


    def execute_routine(self, name_routine:str):
        routine = self._sequence["routines"][name_routine]
        points = self._sequence["points"]
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
  





            
        


    def teach_mode():
        pass






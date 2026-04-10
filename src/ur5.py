import rtde_receive
import rtde_control
import math

class UR5():
<<<<<<< Updated upstream
    "Robot UR5"
    def __init__(self, ip: str, tools: dict["name":"tcp"], workplace: list[float], home: tuple[float], freedom_grades: int):
        tools = UR5._comprobe_tool(tools)
        self._receptor = rtde_receive.RTDEReceiveInterface(ip)
        self._controlador = rtde_control.RTDEControlInterface(ip)
        self._workplace = workplace
        self._tools = tools
        self._active_tool = None
        self._estate = None
        self._tcp = None
        #self._home =  UR5._validate_home(home, freedom_grades)
        self._home = (0, -60, -130, 13, 90, 10)

    @property
    def home(self):
        return self._home
    
    @home.setter
    def home(self, new_home: str):
        self._home = UR5._validate_home(new_home)

    @staticmethod
    def _validate_home(home: tuple[float]):
        for grades_motor in home:
            if not isinstance(grades_motor, float) and 350 < abs(grades_motor) < 0:
                print("Grades of motor aren't invalids.")
                return None
        return home

    @staticmethod
    def _validate_tool(tools: dict["name":"tcp"]):
        validate = False
        tools_validates = {}
        for name, tcp in tools.items():
            if len(tcp) == 6:
                for coord in tcp:
                    if isinstance(coord, int):
                        validate = True
                    tools_validates[name] = tcp

            if validate == True:
                    print(f"{name} was add sucesful.")
                    tools_validates[name] = tcp
            else:
                print(f"{name} was ignored, coordenates invalids.")
        return tools_validates

=======
    def __init__(self, ip: str, tools: dict["name":"tcp"]):
        UR5._comprobe_tool(tools)
        self._receptor = rtde_receive.RTDEReceiveInterface(ip)
        self._controlador = rtde_control.RTDEControlInterface(ip)
        self._entorno = None
        self._tools = tools
        self._active_tool = None
        self._estadp = None
        self._tcp = None
        self._home =  None


    
    @staticmethod
    def _comprobe_tool(tools: dict["name":"tcp"]):
        if len(TCP) == 6:
            return True
        return False

>>>>>>> Stashed changes


    def add_tool(self, tool: str, TCP: tuple[float]):
        if UR5._comprobe_tool(TCP):
            self._tools[tool] = TCP
        else:
<<<<<<< Updated upstream
            print("Tool wasn't add: Coordenates of TCP are invalids")
=======
            print("Tool wasn't add: TCPenates of TCP aren validates")
>>>>>>> Stashed changes


    def change_tool(self, name_tool):
        if name_tool not in self.herramientas:
            print("Tool not defined")
            return False

        new_tcp = self.herramientas[name_tool] 
        self.controlador.setTcp(new_tcp)

        self.active_tool = name_tool

        print("The tool active is:", self.active_tool)
        return True
    
    def consult_tool_activate(self):
        print("Tool active:", self._active_tool)


    def move_to_home(self):
<<<<<<< Updated upstream
        self._controlador.movej(self.home)
=======
        pass
>>>>>>> Stashed changes

        
    def pick_and_place(self):
        pass

    def emergency_stop():
        pass






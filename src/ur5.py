import rtde_receive
import rtde_control

class UR5():
    def __init__(self, ip):
        self.receptor = rtde_receive.RTDEReceiveInterface(ip)
        self.controlador = rtde_control.RTDEControlInterface(ip)
        self.entorno = None
        self.herramientas = {
            "": [],
            "": []
        }
        self.active_tool = None
        self.estadp = None
        self.tcp = None
        self.home =  None

    @property
    def controlador(self):
        return self.controlador
    
    @controlador.setter
    def controlador(self, controlador):
        self.controlador = controlador

    def activar_herramienta(self, name_tool):
        if name_tool not in self.herramientas:
            print("La IA intento usar una herrramienta no definida.")
            return False

        new_tcp = self.herramientas[name_tool] 
        self.controlador.setTcp(new_tcp)

        self.active_tool = name_tool

        print("La herramienta actual es:", self.active_tool)
        return True


    def move_to_home(self):
        

    def change_tool(self):
        self.tcp = tcp
        
    def pick_and_place(self):
        self.controlador.moveJ()
        pass




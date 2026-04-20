from ur5 import UR5
from display import Display



def main():
    ip = "172.17.0.2"
    
    path_json = "/home/ivan/proyectos/ur5/cobogen-ur5/docs/routines.json"

    robot = UR5(ip=ip, home= (-4, -65, -119, -27, 91, 0), path_json=path_json)
    display = Display(robot)
    display.options()




if __name__ == "__main__":
    main()
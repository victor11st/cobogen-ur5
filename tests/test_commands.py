
from src.ur5 import UR5

def main():
    robot = UR5(ip='172.17.0.2', 
                tools={"pinza":(0.0, 0.0, 100, 0.0, 0.0, 0.0)},
                workplace=(0.0, 0.0, 0.0, 0.0), 
                home=(0, -60, -130, 13, 90, 10))
    
    robot.move_to_home()



if __name__ == "__main__":
    main()
import rtde_control
import rtde_receive
import time

IP_ROBOT = "127.0.0.1" 

try:
    rtde_r = rtde_receive.RTDEReceiveInterface(IP_ROBOT)
    rtde_c = rtde_control.RTDEControlInterface(IP_ROBOT)

    # 1. Esperamos a que el robot esté quieto
    print("Esperando estabilización...")
    time.sleep(1)

    # 2. Leemos la posición REAL actual
    pose_leida = rtde_r.getActualTCPPose()
    print(f"TCP LEÍDO -> X: {pose_leida[0]:.4f}, Y: {pose_leida[1]:.4f}, Z: {pose_leida[2]:.4f}")

    # 3. Intentamos movernos a esa MISMA posición
    # Usamos moveL (Lineal) con una velocidad baja para observar
    print("Enviando orden de movimiento al mismo punto...")
    rtde_c.moveL(pose_leida, speed=0.1, acceleration=0.05)

    # 4. Volvemos a leer tras el movimiento
    time.sleep(1)
    nueva_pose = rtde_r.getActualTCPPose()
    print(f"TCP FINAL -> X: {nueva_pose[0]:.4f}, Y: {nueva_pose[1]:.4f}, Z: {nueva_pose[2]:.4f}")

    # 5. Calculamos la diferencia (El error)
    error_x = abs(pose_leida[0] - nueva_pose[0])
    print(f"Error detectado en X: {error_x * 1000:.2f} mm")

except Exception as e:
    print(f"Error: {e}")
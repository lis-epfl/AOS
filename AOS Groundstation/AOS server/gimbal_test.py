import time
import ds_wrapper as w

print("Starting gimbal test...")

drone_id = 1
pitch_increment = 5
max_pitch = 50
min_pitch = -90
update_interval = 0.5 # seconds
waypoint_num = 1


try:
    while True:
        # get the current telemetry data
        image_telemetry_data = w.getImageAndTelemetryData(drone_id)
        telemetry_data = bytearray(image_telemetry_data[3110408:]).decode()
        telemetry_elements = telemetry_data.split(':')

        print(f"Telemetry: {telemetry_elements}")
    
        latitude = telemetry_elements[0]
        longitude = telemetry_elements[1]
        altitude = telemetry_elements[2]
        heading = telemetry_elements[3]
        curr_pitch = float(telemetry_elements[4])
        gimbal_yaw = telemetry_elements[6]
        waypoint_check = telemetry_elements[14]
        next_waypoint = telemetry_elements[15]

        print(f"Current gimbal pitch: {curr_pitch}")

        curr_pitch += pitch_increment

        if curr_pitch > max_pitch or curr_pitch < min_pitch:
            pitch_increment = -pitch_increment
            curr_pitch += pitch_increment

        print(f"Setting gimbal pitch to: {curr_pitch}")

        # Create waypoint data string
        # Format: lat:lon:alt:heading:speed:waypoint_num:threshold:gimbal_pitch:gimbal_yaw:camera
        new_waypoint = f"{latitude}:{longitude}:{altitude}:{heading}:2:{waypoint_num}:2:{str(curr_pitch)}:0:90"
        # new_waypoint = f"0:0:0:0:2:{waypoint_num}:2:{str(curr_pitch)}:0:90"

        result = w.sendWayPointData(new_waypoint, drone_id)
        
        print(f"Telemetry waypoint check: {waypoint_check}, next waypoint: {next_waypoint}, sent waypoint num: {waypoint_num}")

        waypoint_num += 1


        time.sleep(update_interval)
        print("-"*40)

except KeyboardInterrupt:
    print("Gimbal test stopped by user.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    print("Gimbal test finished.")

            
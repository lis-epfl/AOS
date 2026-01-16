import time
import cv2
import base64
import ds_wrapper as w

# Imports for image sharing to memory mapped files
import struct
import mmap
import utils.imageSharingUtil as imageSharingUtil

print("Starting Image test...")

drone_id = 1
num_drones = 1


# Check decoding method
decode = w.isHWDecoderEnabled()

if decode == 1:
    decoding = 'hardware'
elif decode == 0:
    decoding = 'software'
else:
    print('Invalid decoding method')



try:
    while True:

        print("Fetching telemetry data...")

        # get the current telemetry data
        image_telemetry_data = w.getImageAndTelemetryData(drone_id)

        print("Telemetry data fetched.")

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
    
        ####################################### Image Processing #############################################

        # Get the image data from the drones
        if decoding == 'software':
            Image = cv2.cvtColor(image_telemetry_data[0:3110400].reshape(1080*3//2, 1920), cv2.COLOR_YUV420p2RGB)   # for software decoding
        elif decoding == 'hardware':
            Image = cv2.cvtColor(image_telemetry_data[0:3110400].reshape(1080*3//2, 1920), cv2.COLOR_YUV2BGR_NV12) # for hardware decoding
                            
            # Convert the image to base64
        retval, buffer = cv2.imencode('.jpg', Image)
        imgBase64 = base64.b64encode(buffer).decode('utf-8')
        
        ######################################### Image Sharing to Memory Mapped Files ############################################
        
        # Downsize image parameters
        width = 1920
        height = 1080
        depth = 3
        processedImageSize = width * height * depth

        # Resize the image
        Image = cv2.resize(Image, (width, height))

        # Shared memory configuration for multiple images
        metadataSize = 12
        blockSize = metadataSize + processedImageSize
        totalMMFSize = num_drones * blockSize

        # Write the image to shared memory
        try:
            
            print("Writing processed image to shared memory for drone ID:", drone_id)
            
            # Open (or create) the memory mapped file with the total size for all blocks
            processedMMF = mmap.mmap(-1, totalMMFSize, "ProcessedImageSharedMemory")
            
            # Compute the block offset for this droneId (assumed to be in the range [0, numImages-1])
            blockOffset = (drone_id-1) * blockSize

            # Optionally flip the image vertically (as in your original code)
            flipped_image = cv2.flip(Image, 0)

            # Write the memory block (header and image data)
            imageSharingUtil.write_memory(processedMMF, blockOffset, processedImageSize, flipped_image, drone_id-1, float(heading))
            
            # Clean up image if desired
            del Image
        except Exception as e:
            print("Problem opening/reading processed memory")
            print(e)

        ############################################################################################################################


except KeyboardInterrupt:
    print("Image test stopped by user.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    print("Image test finished.")

            
import struct
import mmap

def write_memory(processedMMF, blockOffset, processedImageSize, image_data, droneId, heading):
    """
    Write an image block to shared memory with Unity.

    Block layout:
      - int flag (4 bytes)
      - int droneId (4 bytes)
      - float heading (4 bytes)
      - image data (processedImageSize bytes)
    """
    metadataSize = 12  # 4 bytes flag, 4 bytes droneId, 4 bytes heading
    blockSize = metadataSize + processedImageSize

    while True:
        # Check if Unity is ready (flag == 0)
        processedMMF.seek(blockOffset)
        flag_bytes = processedMMF.read(4)
        if len(flag_bytes) != 4:
            print("Error: Buffer for flag is less than 4 bytes. Buffer length:", len(flag_bytes))
            continue  # Optionally, you could add a short sleep here before retrying.
        flag = struct.unpack('i', flag_bytes)[0]

        if flag == 0:
            # Set flag to 1 (busy writing)
            processedMMF.seek(blockOffset)
            processedMMF.write(struct.pack('i', 1))

            # Write droneId (int) at offset blockOffset + 4
            processedMMF.seek(blockOffset + 4)
            processedMMF.write(struct.pack('i', droneId))

            # Write heading (float) at offset blockOffset + 8
            processedMMF.seek(blockOffset + 8)
            processedMMF.write(struct.pack('f', heading))

            # Convert image to bytes and check size
            image_bytes = image_data.tobytes()
            if len(image_bytes) != processedImageSize:
                raise ValueError(f"Image size mismatch: expected {processedImageSize}, got {len(image_bytes)}")

            # Write image data at offset blockOffset + 12
            processedMMF.seek(blockOffset + 12)
            processedMMF.write(image_bytes)

            # Reset flag to 0 (writing complete)
            processedMMF.seek(blockOffset)
            processedMMF.write(struct.pack('i', 0))
            break
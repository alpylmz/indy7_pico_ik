import serial
import time
import re
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Send a message to a serial device and process multi-line responses. "
                    "Searches for 'Elapsed time: %d us' to mark end of message."
    )
    parser.add_argument(
        '--port', 
        type=str, 
        default="/dev/tty.usbmodem211201",  # Default, common on macOS
        help="Serial port device name (e.g., /dev/tty.usbmodemXXXX, /dev/ttyACM0, COM3)"
    )
    parser.add_argument(
        '--baud', 
        type=int, 
        default=115200, 
        help="Baud rate for serial communication (default: 115200)"
    )
    parser.add_argument(
        '--timeout', 
        type=float, 
        default=40.0,  # Timeout for each readline operation
        help="Timeout in seconds for waiting for each line from the device (default: 1.0)"
    )

    parser.add_argument(
        '--verbose', 
        action='store_true', 
        help="Enable verbose mode to print all lines received from the device"
    )
    
    args = parser.parse_args()

    serial_port = args.port
    baud_rate = args.baud
    read_timeout = args.timeout
    # First three 
    message_to_send = \
    """
    0.5 0.5 0.5
    1.0 0.0 0.0
    0.0 1.0 0.0
    0.0 0.0 1.0
    1.97125 -0.372364 1.64045 -0.674883 2.38533 0.727269
    """

    print(f"Attempting to connect to: {serial_port} at {baud_rate} baud.")
    print(f"Read timeout per line: {read_timeout}s")
    print(f"Message to send: {message_to_send.strip()}")
    if args.verbose:
        print("Verbose mode: ON")
    else:
        print("Verbose mode: OFF (only target line and essential messages will be shown)")

    try:
        # Using 'with' ensures the serial port is closed automatically
        with serial.Serial(serial_port, baud_rate, timeout=read_timeout) as ser:
            print(f"Successfully connected to {serial_port}.")

            # Clear any residual data in buffers
            ser.reset_input_buffer()
            ser.reset_output_buffer()

            # --- Send the message ---
            message_bytes = message_to_send.encode('utf-8')
            ser.write(message_bytes)
            print(f"Message sent to device.")

            # --- Process the multi-line response ---
            print("\n--- Waiting for response from device ---")
            found_target_line = False
            lines_processed = 0

            while True:
                response_bytes = ser.readline() # Reads until '\n' or timeout

                if not response_bytes:
                    # readline() timed out (returned empty bytes)
                    print("--- No more data from device (readline timeout). ---")
                    if not found_target_line:
                        print("Target line 'Elapsed time: ... us' was NOT found in the received block.")
                    break # Exit the reading loop

                lines_processed += 1
                # Decode bytes to string. 'replace' handles potential encoding errors.
                line_str = response_bytes.decode('utf-8', errors='replace').strip()

                if args.verbose:
                    print(f"DEV ({lines_processed}): {line_str}")
                
                # Search for the target pattern "Elapsed time: %d us"
                # The regex (\d+) captures one or more digits.
                match = re.search(r"Elapsed time: (\d+) us", line_str)
                
                if match:
                    elapsed_microseconds = match.group(1) # Get the captured digits
                    found_target_line = True
                    
                    # Always print the target line info, as it's key
                    print(f"TARGET FOUND: {line_str}")
                    print(f"==> Extracted Elapsed Time: {elapsed_microseconds} microseconds")
                    return elapsed_microseconds
                    print("--- End of expected message block. ---")
                    break # Exit the reading loop as the target is found
                else:
                    # If not in verbose mode, other lines are skipped (not printed here)
                    # In verbose mode, they were already printed above.
                    pass
            
            if lines_processed == 0 and not found_target_line:
                 print("No response data received from the device at all.")


    except serial.SerialException as e:
        print(f"\nSERIAL ERROR: Could not open or communicate on port {serial_port}.")
        print(f"Details: {e}")
        print("\nPlease check:")
        print("1. Is the device connected and powered on?")
        print(f"2. Is '{serial_port}' the correct port name? (e.g., /dev/ttyACM0, COM3)")
        print("3. Do you have permissions to access the port? (e.g., member of 'dialout' on Linux)")
        print("4. Is another program using the port?")
        print(f"5. Is the baud rate ({baud_rate}) correct?")
    except Exception as e:
        print(f"\nUNEXPECTED ERROR: {e}")

if __name__ == "__main__":
    all_microseconds = []
    elapsed_time = main()
    all_microseconds.append(float(elapsed_time))





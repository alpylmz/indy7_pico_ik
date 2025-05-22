With this project, you can offload the computation of inverse kinematics to pico.

1. Check https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf, download and test the Raspberry Pi Pico VS Code extension.
2. Create a new project with hello_usb example.
3. Add the following to the CMakeLists.txt file, right after the `set(CMAKE_EXPORT_COMPILE_COMMANDS ON)` line:
```cmake
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")
set(CMAKE_C_FLAGS_RELEASE "-O3 -DNDEBUG")
set(PICO_COPY_TO_RAM 1)
```
4. In CMakeLists.txt, change all instances of `hello_usb.c` to `hello_usb.cpp`.
5. Copy the contents of the repo and paste it to the project folder.
6. Read `serial_test.py`. You will need to change the serial port to match it to your system.
7. Also see message_to_send variable in the same file, you need to modify it to match your needs.
8. Compile and run the pico project.
9. Run `python3 serial_test.py --verbose` to start the serial communication test. The current parameters should successfully converge and you should be able to see: 
```
DEV (1): Output joint angles: 1.102027 -1.011385 -1.089235 0.093929 2.143987 -1.054478
```
10. Integrate serial_test.py into your project.

If you have any questions, feel free to ping me.


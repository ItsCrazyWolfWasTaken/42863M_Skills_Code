from vex import *
# allows everything to import properly and calibrate
wait(30, MSEC)

# declaring the brain and controller
brain=Brain()
controller_1 = Controller(PRIMARY)
# declaring the pneumatic piston
digital_out_a = DigitalOut(brain.three_wire_port.a)
# declaring the motors (left_a and left_b are the front and back of the left side of the drivetrain, respectively)
left_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
left_b = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
# declaring the motors(right_a and right_b are the front and back of the right side of the drivetrain, respectively)
right_a = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
right_b = Motor(Ports.PORT19, GearSetting.RATIO_18_1, True)
# declaring the motors (left_intake and right_intake are the left and right intake motors, respectively)
left_intake = Motor(Ports.PORT16, GearSetting.RATIO_18_1, False)
right_intake = Motor(Ports.PORT15, GearSetting.RATIO_18_1, True)
# declaring the motors (left_redirect and right_redirect are the left and right redirect motors, respectively)
left_redirect = Motor(Ports.PORT17, GearSetting.RATIO_36_1, False)
right_redirect = Motor(Ports.PORT18, GearSetting.RATIO_36_1, True)
# declaring the motor groups (left_motors and right_motors are the left and right side of the drivetrain, respectively)
left_motors = MotorGroup(left_a, left_b)
right_motors = MotorGroup(right_a, right_b)
# declaring the motor groups (redirect_motors is the intake and redirect motors)
redirect_motors = MotorGroup(left_intake, right_intake, left_redirect, right_redirect)
# declaring the drivetrain
drivetrain = DriveTrain(left_motors, right_motors, 319.19, 295, 40, MM, 1)

def pre_autonomous():
    brain.screen.clear_screen()
    # prints for debugging to check if it is running
    brain.screen.print("pre auton code")
    wait(1, SECONDS)

def autonomous():
    brain.screen.clear_screen()
    # prints for debugging to check if it is running
    brain.screen.print("autonomous code")
    # makes sure that the drivetrain doesn't drive too fast
    drivetrain.set_drive_velocity(85, PERCENT)
    # speeds up the redirect motors
    redirect_motors.set_velocity(100, PERCENT)
    # backs robot into mobile goal
    drivetrain.drive_for(FORWARD, 8, INCHES)
    # grabs mobile goal
    digital_out_a.set(True)
    # spins redirect motors to score preload on the mobile goal
    redirect_motors.spin(REVERSE)
    # turns to move to corner
    drivetrain.turn_for(LEFT, 125, DEGREES)
    # moves to corner
    drivetrain.drive_for(FORWARD, 26, INCHES)
    # stops the redirect motors
    redirect_motors.stop()
    # releases the mobile goal
    digital_out_a.set(False)
    # makes it move slightly slower so as not to keep the goal by accident
    drivetrain.set_drive_velocity(50, PERCENT)
    # making sure aligned s
    drivetrain.turn_for(LEFT, 30, DEGREES)
    # moves back in line with the other goal
    drivetrain.drive_for(REVERSE, 24, INCHES)
    # goes back to normal speed
    drivetrain.set_drive_velocity(85, PERCENT)
    # turns to face the goal
    drivetrain.turn_for(LEFT, 155, DEGREES)
    # backs up to the goal
    drivetrain.drive_for(FORWARD, 60, INCHES)
    # grabs mobile goal
    digital_out_a.set(True)
    # turns to face corner
    drivetrain.turn_for(RIGHT, 25, DEGREES)
    # puts goal in corner
    drivetrain.drive_for(FORWARD, 30, INCHES)

def user_control():
    while True:
        # sets speed based off of controller positions for the sides
        # the negative is to make the motors spin in the correct direction
        left_motors.set_velocity(-1*(controller_1.axis2.position() + controller_1.axis4.position()/2), PERCENT)
        # the division of two is to lower turn sensitivity
        right_motors.set_velocity(-1*(controller_1.axis2.position() - controller_1.axis4.position()/2), PERCENT)

        # make the sides actually spin
        left_motors.spin(FORWARD)
        right_motors.spin(FORWARD)

        # sets the speed of the intake/redirect motors so they spin faster
        redirect_motors.set_velocity(100, PERCENT)
        # press buttons (R2 to spin forward, R1 to spin backward, A to stop) on controller to spin the redirect motors
        if controller_1.buttonR1.pressing():
            redirect_motors.spin(REVERSE)
        elif controller_1.buttonR2.pressing():
            redirect_motors.spin(FORWARD)
        elif controller_1.buttonA.pressing():
            redirect_motors.stop()
    
        # press buttons (L2 to lower, L1 to raise) on controller to lower/raise goal holder
        if controller_1.buttonL2.pressing():
            digital_out_a.set(True)
        if controller_1.buttonL1.pressing():
            digital_out_a.set(False)

        # updates every 20 milliseconds
        wait(20, MSEC)

# create competition instance
comp = Competition(user_control, autonomous)
pre_autonomous()
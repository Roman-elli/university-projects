import config as cfg

from engine.actions import (
    turn_left_with_full_power,
    turn_left_with_partial_power,
    turn_right_with_full_power,
    turn_right_with_partial_power,
    main_engine_full_power,
    main_engine_parcial_power,
)
from engine.perceptions import (
    horizontal_position,
    horizontal_velocity,
    vertical_velocity,
    orientation,
    left_foot_touch,
    right_foot_touch,
)

def agent_no_wind(observation):
    action = [0, 0]

    horizontal_vel = horizontal_velocity(observation)
    vertical_vel = vertical_velocity(observation)
    orientation_var = orientation(observation)
    horizontal_pos = horizontal_position(observation)

    # 1. Final case
    # PE, PD -> NIL
    if left_foot_touch(observation) and right_foot_touch(observation):
        return action

    # 2. ABOVE THE EXTERNAL HORIZONTAL SPEED TO THE RIGHT AND CORRECT DEGREE
    # VH > LHE, O < 1.8 * LAE, VV < LV -> GET, MP
    # VH > LHE, O < 1.8 * LAE -> GET
    elif horizontal_vel > cfg.EXTERN_HORIZONTAL_VELOCITY_THRESHOLD and orientation_var < 1.8 * cfg.EXTERN_ANGLE_THRESHOLD and vertical_vel < cfg.VERTICAL_VELOCITY_THRESHOLD:
        action = turn_left_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_vel > cfg.EXTERN_HORIZONTAL_VELOCITY_THRESHOLD and orientation_var < 1.8 * cfg.EXTERN_ANGLE_THRESHOLD:
        action = turn_left_with_full_power(action)

    # 3. ABOVE THE EXTERNAL HORIZONTAL SPEED TO THE RIGHT AND INCORRECT DEGREE
    # VH > LHE, VV < LV -> GDT, MP
    # VH > LHE -> GDT
    elif horizontal_vel > cfg.EXTERN_HORIZONTAL_VELOCITY_THRESHOLD and vertical_vel < cfg.VERTICAL_VELOCITY_THRESHOLD:
        action = turn_right_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_vel > cfg.EXTERN_HORIZONTAL_VELOCITY_THRESHOLD:
        action = turn_right_with_full_power(action)

    # 4. ABOVE THE EXTERNAL HORIZONTAL SPEED TO THE LEFT AND CORRECT DEGREE
    # VH < -LHE, O > -1.8 * LAE, VV < LV -> GDT, MP
    # VH < -LHE, O > -1.8 * LAE -> GDT
    elif horizontal_vel < -cfg.EXTERN_HORIZONTAL_VELOCITY_THRESHOLD and orientation_var > -1.8 * cfg.EXTERN_ANGLE_THRESHOLD and vertical_vel < cfg.VERTICAL_VELOCITY_THRESHOLD:
        action = turn_right_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_vel < -cfg.EXTERN_HORIZONTAL_VELOCITY_THRESHOLD and orientation_var > -1.8 * cfg.EXTERN_ANGLE_THRESHOLD:
        action = turn_right_with_full_power(action)

    # 5. ABOVE THE EXTERNAL HORIZONTAL SPEED TO THE LEFT AND INCORRECT DEGREE
    # VH < -LHE, VV < LV -> GET, MP
    # VH < -LHE -> GET
    elif horizontal_vel < -cfg.EXTERN_HORIZONTAL_VELOCITY_THRESHOLD and vertical_vel < cfg.VERTICAL_VELOCITY_THRESHOLD:
        action = turn_left_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_vel < -cfg.EXTERN_HORIZONTAL_VELOCITY_THRESHOLD:
        action = turn_left_with_full_power(action)

    # 6. OUT OF BOUNDS THE LEFT AND THE RIGHT DEGREE
    # H < -LH, O > -LAE, VV < LV -> GDT, MP
    # H < -LH, O > -LAE -> GDT
    elif horizontal_pos < -cfg.HORIZONTAL_THRESHOLD and orientation_var > -cfg.EXTERN_ANGLE_THRESHOLD and vertical_vel < cfg.VERTICAL_VELOCITY_THRESHOLD:
        action = turn_right_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_pos < -cfg.HORIZONTAL_THRESHOLD and orientation_var > -cfg.EXTERN_ANGLE_THRESHOLD:
        action = turn_right_with_full_power(action)

    # 7. OUT OF BOUNDS THE LEFT AND THE INCORRECT DEGREE
    # H < -LH, VV < LV -> GET, MP
    # H < -LH -> GET
    elif horizontal_pos < -cfg.HORIZONTAL_THRESHOLD and vertical_vel < cfg.VERTICAL_VELOCITY_THRESHOLD:
        action = turn_left_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_pos < -cfg.HORIZONTAL_THRESHOLD:
        action = turn_left_with_full_power(action)

    # 8. OUT OF BOUNDS THE RIGHT AND THE CORRECT DEGREE
    # H > LH, O < LAE, VV < LV -> GET, MP
    # H > LH, O < LAE -> GET
    elif horizontal_pos > cfg.HORIZONTAL_THRESHOLD and orientation_var < cfg.EXTERN_ANGLE_THRESHOLD and vertical_vel < cfg.VERTICAL_VELOCITY_THRESHOLD:
        action = turn_left_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_pos > cfg.HORIZONTAL_THRESHOLD and orientation_var < cfg.EXTERN_ANGLE_THRESHOLD:
        action = turn_left_with_full_power(action)

    # 9. OUT OF BOUNDS THE RIGHT AND THE INCORRECT DEGREE
    # H > LH, VV < LV -> GDT, MP
    # H > LH -> GDT 
    elif horizontal_pos > cfg.HORIZONTAL_THRESHOLD and vertical_vel < cfg.VERTICAL_VELOCITY_THRESHOLD:
        action = turn_right_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_pos > cfg.HORIZONTAL_THRESHOLD:
        action = turn_right_with_full_power(action)

    # 10. ABOVE THE HORIZONTAL SPEED LIMIT TO THE RIGHT PERMITTED INTERNALLY WITH CORRECT GRADE
    # VH > LVH, O < Θ, VV < LV -> GET, MP
    # H > LVH, O < Θ -> GET
    elif horizontal_vel > cfg.HORIZONTAL_VELOCITY_THRESHOLD and orientation_var < cfg.ANGLE_THRESHOLD and vertical_vel < cfg.VERTICAL_VELOCITY_THRESHOLD:
        action = turn_left_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_vel > cfg.HORIZONTAL_VELOCITY_THRESHOLD and orientation_var < cfg.ANGLE_THRESHOLD:
        action = turn_left_with_full_power(action)

    # 11. ABOVE THE HORIZONTAL SPEED LIMIT ON THE RIGHT PERMITTED INTERNALLY WITH INCORRECT GRADE
    # VH > LVH, VV < LV -> GDT, MP
    # VH > LVH -> GDT
    elif horizontal_vel > cfg.HORIZONTAL_VELOCITY_THRESHOLD and vertical_vel < cfg.VERTICAL_VELOCITY_THRESHOLD:
        action = turn_right_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_vel > cfg.HORIZONTAL_VELOCITY_THRESHOLD:
        action = turn_right_with_full_power(action)

    # 12. ABOVE THE HORIZONTAL SPEED LIMIT ON THE LEFT PERMITTED INTERNALLY WITH CORRECT GRADE
    # VH < -LVH, O > -Θ, VV < LV -> GDT, MP
    # VH < -LVH, O > -Θ -> GDT
    elif horizontal_vel < -cfg.HORIZONTAL_VELOCITY_THRESHOLD and orientation_var > -cfg.ANGLE_THRESHOLD and vertical_vel < cfg.VERTICAL_VELOCITY_THRESHOLD:
        action = turn_right_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_vel < -cfg.HORIZONTAL_VELOCITY_THRESHOLD and orientation_var > -cfg.ANGLE_THRESHOLD:
        action = turn_right_with_full_power(action)

    # 13.ABOVE THE HORIZONTAL SPEED LIMIT ON THE LEFT PERMITTED INTERNALLY WITH INCORRECT DEGREE
    # VH < -LVH, VV < LV -> GET, MP
    # VH < -LVH -> GET
    elif horizontal_vel < -cfg.HORIZONTAL_VELOCITY_THRESHOLD and vertical_vel < cfg.VERTICAL_VELOCITY_THRESHOLD:
        action = turn_left_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_vel < -cfg.HORIZONTAL_VELOCITY_THRESHOLD:
        action = turn_left_with_full_power(action)

    # 14. STRONG CORRECTION TO THE RIGHT ON THE DESCENT AT THE CORRECT POINT
    # O > 4 * Θ, VV < LV -> GDT, MP 
    # O > 4 * Θ -> GDT
    elif orientation_var > 4 * cfg.ANGLE_THRESHOLD and vertical_vel < cfg.VERTICAL_VELOCITY_THRESHOLD:
        action = turn_right_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif orientation_var > 4 * cfg.ANGLE_THRESHOLD:
        action = turn_right_with_full_power(action)

    # 15. STRONG CORRECTION TO THE LEFT ON THE DESCENT AT THE CORRECT POINT
    # O < -4 * Θ, VV < LV -> GET, MP
    # O < -4 * Θ -> GET
    elif orientation_var < -4 * cfg.ANGLE_THRESHOLD and vertical_vel < cfg.VERTICAL_VELOCITY_THRESHOLD:
        action = turn_left_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif orientation_var < -4 * cfg.ANGLE_THRESHOLD:
        action = turn_left_with_full_power(action)

    # 16. WEAK CORRECTION TO THE RIGHT ON THE DESCENT AT THE CORRECT POINT
    # O < -Θ, VV < LV -> GDP, MP
    # O < -Θ -> GDP
    elif orientation_var < -cfg.ANGLE_THRESHOLD and vertical_vel < cfg.VERTICAL_VELOCITY_THRESHOLD:
        action = turn_right_with_partial_power(action)
        action = main_engine_parcial_power(action)
    elif orientation_var < -cfg.ANGLE_THRESHOLD:
        action = turn_right_with_partial_power(action)
    
    # 17. WEAK CORRECTION TO THE LEFT ON THE DOWNTREND AT THE CORRECT POINT
    # O > Θ, VV < LV -> GEP, MP
    # O > Θ -> GEP
    elif orientation_var > cfg.ANGLE_THRESHOLD and vertical_vel < cfg.VERTICAL_VELOCITY_THRESHOLD:
        action = turn_left_with_partial_power(action)
        action = main_engine_parcial_power(action)
    elif orientation_var > cfg.ANGLE_THRESHOLD:
        action = turn_left_with_partial_power(action)
    
    if action == [0, 0]:
        action = cfg.env.action_space.sample()
    
    return action

def agent_wind(observation):
    action = [0, 0]

    # Both feet of the spacecraft touch
    if left_foot_touch(observation) == True and right_foot_touch(observation) == True: return action

    # EXCEEDS THE MAXIMUM SPEED LIMIT ON THE RIGHT
    elif(horizontal_velocity(observation) > 2*cfg.WIND_EXTERN_HORIZONTAL_VELOCITY_THRESHOLD):
        # STEERS TO THE LEFT
        if orientation(observation) < 3.1 * cfg.WIND_EXTERN_ANGLE_THRESHOLD:
            action = turn_left_with_full_power(action)
        elif orientation(observation) > 3.3 * cfg.WIND_EXTERN_ANGLE_THRESHOLD: action = turn_right_with_full_power(action)
        # TOTAL VERTICAL SPEED
        if vertical_velocity(observation) < 6 * cfg.WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_full_power(action)
        # PARTIAL VERTICAL SPEED
        elif vertical_velocity(observation) < 5 * cfg.WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_parcial_power(action)

    # EXCEEDS THE MAXIMUM SPEED LIMIT ON THE LEFT 
    elif(horizontal_velocity(observation) < -2*cfg.WIND_EXTERN_HORIZONTAL_VELOCITY_THRESHOLD): 
        # STEER RIGHT
        if orientation(observation) > -3.1 * cfg.WIND_EXTERN_ANGLE_THRESHOLD:
            action = turn_right_with_full_power(action)
        elif orientation(observation) < -3.3 * cfg.WIND_EXTERN_ANGLE_THRESHOLD: action = turn_left_with_full_power(action)
        # TOTAL VERTICAL SPEED
        if vertical_velocity(observation) < 6 * cfg.WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_full_power(action)
        # PARTIAL VERTICAL SPEED
        elif vertical_velocity(observation) < 5 * cfg.WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_parcial_power(action)        

    # OUT OF BOUNDS THE LEFT
    elif(horizontal_position(observation) < -cfg.WIND_HORIZONTAL_THRESHOLD):
        # GUIDES THE RIGHT
        if orientation(observation) > -2.7 * cfg.WIND_EXTERN_ANGLE_THRESHOLD: action = turn_right_with_full_power(action)
        elif orientation(observation) < -2.8 * cfg.WIND_EXTERN_ANGLE_THRESHOLD: action = turn_left_with_full_power(action)

        # TOTAL VERTICAL SPEED
        if vertical_velocity(observation) < 4 * cfg.WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_full_power(action)
        # PARTIAL VERTICAL SPEED
        elif vertical_velocity(observation) < 3*cfg.WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_parcial_power(action)
    
    # OUT OF BOUNDS THE RIGHT
    elif(horizontal_position(observation) > cfg.WIND_HORIZONTAL_THRESHOLD):
        # LEFT-WING GUIDANCE
        if orientation(observation) < 2.7 * cfg.WIND_EXTERN_ANGLE_THRESHOLD: action = turn_left_with_full_power(action)
        elif orientation(observation) > 2.8 * cfg.WIND_EXTERN_ANGLE_THRESHOLD: action = turn_right_with_full_power(action)

        # TOTAL VERTICAL SPEED
        if vertical_velocity(observation) < 4 * cfg.WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action[0] = main_engine_full_power(action)[0]
        # PARTIAL VERTICAL SPEED
        elif vertical_velocity(observation) < 3 * cfg.WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action[0] = main_engine_parcial_power(action)[0]

    # ABOVE THE HORIZONTAL SPEED LIMIT ON THE RIGHT PERMITTED INTERNALLY
    elif(horizontal_velocity(observation) > cfg.WIND_HORIZONTAL_VELOCITY_THRESHOLD):
        # LEFT-WING GUIDANCE
        if orientation(observation) < cfg.WIND_ANGLE_THRESHOLD: action = turn_left_with_full_power(action)
        elif orientation(observation) > 1.2 * cfg.WIND_ANGLE_THRESHOLD: action = turn_right_with_full_power(action)

        # TOTAL VERTICAL SPEED
        if vertical_velocity(observation) < 4 * cfg.WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_full_power(action)
        # PARTIAL VERTICAL SPEED
        elif vertical_velocity(observation) < 3 * cfg.WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_parcial_power(action)
        
    # ABOVE THE HORIZONTAL SPEED LIMIT ON THE LEFT PERMITTED INTERNALLY
    elif(horizontal_velocity(observation) < -cfg.WIND_HORIZONTAL_VELOCITY_THRESHOLD): 
        # GUIDES THE RIGHT
        if orientation(observation) > -cfg.WIND_ANGLE_THRESHOLD: action = turn_right_with_full_power(action)
        elif orientation(observation) < -1.2 * cfg.WIND_ANGLE_THRESHOLD: action = turn_left_with_full_power(action)

        # TOTAL VERTICAL SPEED
        if vertical_velocity(observation) < 4 * cfg.WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_full_power(action)
        # PARTIAL VERTICAL SPEED
        elif vertical_velocity(observation) < 3 * cfg.WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_parcial_power(action)

    # STRONGLY GUIDES THE RIGHT INTERNALLY
    elif orientation(observation) > 2.5 * cfg.WIND_ANGLE_THRESHOLD:
        action = turn_right_with_full_power(action)
        # TOTAL VERTICAL SPEED
        if vertical_velocity(observation) < 5 * cfg.WIND_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_full_power(action)
        # PARTIAL VERTICAL SPEED
        elif vertical_velocity(observation) < 4*cfg.WIND_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_parcial_power(action)

    # STRONGLY GUIDES THE LEFT INTERNALLY
    elif orientation(observation) < -2.5 * cfg.WIND_ANGLE_THRESHOLD:
        action = turn_left_with_full_power(action)
        # TOTAL VERTICAL SPEED
        if vertical_velocity(observation) < 5 * cfg.WIND_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_full_power(action)
            
        # PARTIAL VERTICAL SPEED
        elif vertical_velocity(observation) < 4 * cfg.WIND_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_parcial_power(action)
    
    # PARTIAL LEFT INTERNAL GUIDANCE
    elif orientation(observation) > cfg.WIND_ANGLE_THRESHOLD:
        action = turn_left_with_partial_power(action)

        # TOTAL VERTICAL SPEED
        if vertical_velocity(observation) < 4 * cfg.WIND_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_full_power(action)
        # PARTIAL VERTICAL SPEED
        elif vertical_velocity(observation) < 3*cfg.WIND_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_parcial_power(action)
    
    # PARTIAL RIGHT INTERNAL GUIDE
    elif orientation(observation) < -cfg.WIND_ANGLE_THRESHOLD:
        action = turn_right_with_partial_power(action)

        # TOTAL VERTICAL SPEED
        if vertical_velocity(observation) < 4 * cfg.WIND_VERTICAL_VELOCITY_THRESHOLD:
            action[0] = main_engine_full_power(action)[0]
        # PARTIAL VERTICAL SPEED
        elif vertical_velocity(observation) < 3*cfg.WIND_VERTICAL_VELOCITY_THRESHOLD:
            action[0] = main_engine_parcial_power(action)[0]

    # Ensures that there is a defined action
    if action == [0, 0]:
        action = cfg.env.action_space.sample()

    return action

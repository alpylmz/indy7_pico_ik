/**
 * Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include <stdio.h>
#include "pico/stdlib.h"
#include "inverse_kinematics/inverse_kinematics.hpp"

const bool BENCHMARK = true;

int main() {
    stdio_init_all();

    double goal_position[3] = {0.0, 0.0, 0.0};
    double goal_rotation[3][3] = {
        {1.0, 0.0, 0.0},
        {0.0, 1.0, 0.0},
        {0.0, 0.0, 1.0}
    };
    double q_start[6] = {0.0, 0.0, 0.0, 0.0, 0.0};
    double q_out[6] = {0.0, 0.0, 0.0, 0.0, 0.0};
    while(true){
        // get goal_position
        for(int i = 0; i < 3; i++){
            scanf("%lf", &goal_position[i]);
        }
        // get goal_rotation
        for(int i = 0; i < 3; i++){
            for(int j = 0; j < 3; j++){
                scanf("%lf", &goal_rotation[i][j]);
            }
        }
        // get q_start
        for(int i = 0; i < 6; i++){
            scanf("%lf", &q_start[i]);
        }

        // Call the inverse_kinematics function
        absolute_time_t start = get_absolute_time();
        inverse_kinematics(goal_position, goal_rotation, q_start, q_out);
        absolute_time_t end = get_absolute_time();

        // Print the output joint angles
        printf("Output joint angles: ");
        for (int i = 0; i < 6; i++) {
            printf("%f ", q_out[i]);
        }
        printf("\n");

        // Print the time taken
        printf("Elapsed time: %lld us\n", absolute_time_diff_us(start, end));

        
    }




}

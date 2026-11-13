import os

from DSP_Assignment_4 import (ReadSignalFile, delay, advance, moving_average, 
                            first_derivative, second_derivative, convolution, Compare_Signals)

def run_tests():
    # 1. Moving Average Test 1 (Window = 3)
    print("1. Testing Moving Average (Window = 3)...")
    idx_ma, samp_ma = ReadSignalFile("Tests/Moving_Avg_TestCases/MovingAvg_input.txt")
    res_ma_3 = moving_average(samp_ma, 3)
    Compare_Signals("Tests/Moving_Avg_TestCases/MovingAvg_out1.txt", idx_ma[:len(res_ma_3)], res_ma_3)
    print("-" * 40)

    # 2. Moving Average Test 2 (Window = 5)
    print("2. Testing Moving Average (Window = 5)...")
    res_ma_5 = moving_average(samp_ma, 5)
    Compare_Signals("Tests/Moving_Avg_TestCases/MovingAvg_out2.txt", idx_ma[:len(res_ma_5)], res_ma_5)
    print("-" * 40)

    # 3. First Derivative Test
    print("3. Testing First Derivative...")
    idx_dev, samp_dev = ReadSignalFile("Tests/Derivative_TestCases/Derivative_input.txt")
    res_first_dev = first_derivative(samp_dev)
    Compare_Signals("Tests/Derivative_TestCases/1st_derivative_out.txt", idx_dev[:len(res_first_dev)], res_first_dev)
    print("-" * 40)

    # 4. Second Derivative Test
    print("4. Testing Second Derivative...")
    res_second_dev = second_derivative(samp_dev)
    Compare_Signals("Tests/Derivative_TestCases/2nd_derivative_out.txt", idx_dev[:len(res_second_dev)], res_second_dev)
    print("-" * 40)

    # 5. Convolution Test
    print("5. Testing Convolution...")
    idx_conv1, samp_conv1 = ReadSignalFile("Tests/Convolution_TestCases/Signal 1.txt")
    idx_conv2, samp_conv2 = ReadSignalFile("Tests/Convolution_TestCases/Signal 2.txt")
    res_idx_conv, res_samp_conv = convolution(idx_conv1, samp_conv1, idx_conv2, samp_conv2)
    Compare_Signals("Tests/Convolution_TestCases/Conv_output.txt", res_idx_conv, res_samp_conv)
    print("-" * 40)

    # 6. Shifting Test (Delay +500)
    # print("6. Testing Delay Shifting (+500)...")
    # idx_shift, samp_shift = ReadSignalFile("Tests/Shifting_TestCases/Input Shifting.txt")
    # res_idx_delay, res_samp_delay = delay(idx_shift, samp_shift, 500)
    # Compare_Signals("Tests/Shifting_TestCases/Signal3.txt", res_idx_delay, res_samp_delay)
    # print("========================================")

if __name__ == '__main__':
    run_tests()
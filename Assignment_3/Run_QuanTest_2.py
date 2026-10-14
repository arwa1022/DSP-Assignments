import os
from DSP_Assignment_3 import quantize_signal
from Tests.Test_2.QuanTest2 import QuantizationTest2

def run_second_test():
    input_file = os.path.join('Tests', 'Test_2', 'Quan2_input.txt')
    output_file = os.path.join('Tests', 'Test_2', 'Quan2_Out.txt')
    
    samples = []
    
    # read the samples from the input file
    with open(input_file, 'r') as f:
        lines = f.readlines()
        # the first 3 lines are configuration/metadata. Data starts at line 4 (index 3).
        for line in lines[3:]:
            line = line.strip()
            if line:  # ensure the line is not empty
                # split by space because the format is "index value" (e.g., "0 -1.22")
                parts = line.split(' ')
                if len(parts) == 2:
                    sample_value = float(parts[1]) # we only need the sample value
                    samples.append(sample_value)
                    
    # فest 2 requires num of levels = 4
    num_levels = 4
    
    # call logic function
    results = quantize_signal(samples, choice_type='levels', user_value=num_levels)
    
    # extract the required results for the test
    your_interval_indices = results['interval_indices']
    your_encoded_values = results['encoded_values']
    your_quantized_values = results['quantized_values']
    your_sampled_error = results['error_values']
    
    # run the validation function
    print("Running Test 2 (Levels)...")
    QuantizationTest2(output_file, your_interval_indices, your_encoded_values, your_quantized_values, your_sampled_error)

if __name__ == '__main__':
    run_second_test()
import os
from DSP_Assignment_3 import quantize_signal
from Tests.Test_1.QuanTest1 import QuantizationTest1

def run_first_test():
    input_file = os.path.join('Tests', 'Test_1', 'Quan1_input.txt')
    output_file = os.path.join('Tests', 'Test_1', 'Quan1_Out.txt')
    
    samples = []
    
    # read the samples from the input file
    with open(input_file, 'r') as f:
        lines = f.readlines()
        # the first 3 lines are configuration/metadata. data starts at line 4 (index 3).
        for line in lines[3:]:
            line = line.strip()
            if line:  # ensure the line is not empty
                # split by space because the format is "index value" (e.g., "0 0.387")
                parts = line.split(' ')
                if len(parts) == 2:
                    sample_value = float(parts[1]) # we only need the sample value
                    samples.append(sample_value)
                    

    # test 1 requires num of bits = 3
    num_bits = 3
    
    # call logic function
    results = quantize_signal(samples, choice_type='bits', user_value=num_bits)
    
    # extract the required results for the test
    your_encoded_values = results['encoded_values']
    your_quantized_values = results['quantized_values']
    
    # run the validation function
    print("Running Test 1 (Bits)...")
    QuantizationTest1(output_file, your_encoded_values, your_quantized_values)

if __name__ == '__main__':
    run_first_test()
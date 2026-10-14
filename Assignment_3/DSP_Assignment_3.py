import math

def calculate_levels(num_of_bits):
    levels = int(math.pow(2, num_of_bits))
    return levels


def calculate_bits_per_level(levels):
    bitsPerLevel = int(math.ceil(math.log2(levels)))
    return bitsPerLevel


def calculate_delta(max_value, min_value, levels):
    delta = (max_value - min_value) / levels
    return delta


def find_ranges(min_value,delta,levels):
    ranges = []
    for i in range(levels):
        lower_limit = min_value + (i * delta) # at i = 0, lower_limit = min_value
        upper_limit = min_value + ((i + 1) * delta) # at i = 0, upper_limit = min_value + delta
        ranges.append((lower_limit, upper_limit))
    return ranges


def find_midpoints(ranges):
    midpoints = []
    for lower_limit, upper_limit in ranges:
        midpoint = (lower_limit + upper_limit) / 2 # mid = (starts + end) / 2
        midpoints.append(midpoint)
    return midpoints


def find_interval_indices(ranges, samples):
    interval_indices = []
    for sample in samples:
        for i, (lower_limit, upper_limit) in enumerate(ranges):
            if lower_limit <= sample < upper_limit:  # Use '<' for upper limit to avoid overlap
                interval_indices.append(i)
                break
        else:
            # if the sample is equal to the maximum value, assign it to the last interval
            if math.isclose(sample, ranges[-1][1], abs_tol=1e-5) or sample >= ranges[-1][1]:
                interval_indices.append(len(ranges) - 1)
            else:
                raise ValueError(f"Sample {sample} is out of range.")
    return interval_indices


def calculate_error(samples, midpoints):
    eq_n = [] # eq(n) = xq(n) - x(n)
    eq_n_pow_2 = [] # eq(n)^2 = (xq(n) - x(n))^2
    sum_of_errors = 0
    for i in range(len(samples)):
        error = midpoints[i] - samples[i]
        error_pow_2 = math.pow(error, 2)
        
        sum_of_errors += error_pow_2

        eq_n.append(error)
        eq_n_pow_2.append(error_pow_2)

    avg_error = sum_of_errors / len(samples) # avg_error = (1/N) * sum(eq(n)^2)

    return eq_n, eq_n_pow_2, sum_of_errors, avg_error


def encode_levels(interval_indices, bits_per_level):
    encoded_values = []
    for index in interval_indices:
        binary_string_with_0b = bin(index) # convert index to binary (ex. 2 becomes '0b10')
        clean_binary = binary_string_with_0b[2:] # remove the '0b' prefix

        # add zeros to the left to match the required bits
        final_encoded_string = clean_binary.zfill(bits_per_level)

        encoded_values.append(final_encoded_string)
    return encoded_values


def quantize_signal(samples, choice_type, user_value):
    # find min & max A
    min_value = min(samples)
    max_value = max(samples)


    if choice_type == 'bits': # calculate levels if you were given bits
        num_of_bits = int(user_value)
        levels = calculate_levels(num_of_bits)
    elif choice_type == 'levels': # calcualate bits per level if you were given levels
        levels = int(user_value)
        num_of_bits = calculate_bits_per_level(levels)
        
    # calculate delta, ranges, and midpoints
    delta = calculate_delta(max_value, min_value, levels)
    ranges = find_ranges(min_value, delta, levels)
    midpoints = find_midpoints(ranges)
    
    # map each sample to its corresponding interval index ( zero-based interval_indices )
    interval_indices = find_interval_indices(ranges, samples)
    
    # assign the quantized values (midpoints) to the samples
    quantized_values = []
    for index in interval_indices:
        quantized_values.append(midpoints[index])
        
    # calculate error
    eq_n, eq_n_pow_2, sum_of_errors, avg_error = calculate_error(samples, quantized_values)
    
    # adjust interval_indices to be 1-based
    one_based_interval_indices = []
    for index in interval_indices:
        one_based_interval_indices.append(index + 1)

    # encode the indices to binary strings
    encoded_values = encode_levels(interval_indices, num_of_bits)

    return {
        'interval_indices': one_based_interval_indices, 'encoded_values': encoded_values, 'quantized_values': quantized_values,
        'error_values': eq_n, 'average_error': avg_error, 'ranges': ranges
    }
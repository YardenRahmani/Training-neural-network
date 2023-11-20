import subprocess
import os
import random

LEARNING_RATES = [pow(10, -x) for x in range(5)]
HIDDEN_LAYER_SIZE = [8,4]
SAMPLES = 1000
SAMPLES_RANGE = 10
EPOCHES = 1000

def generate_data(testNum):
    fileName = "data" + str(testNum)
    with open(fileName, "w") as dataFile:
        if testNum == 1 or testNum == 3:
            inputSize = 1
        elif testNum == 2 or testNum == 4:
            inputSize = 2
        outputSize = 1
        for _ in range(SAMPLES):
            x1 = (SAMPLES_RANGE/2)*random.random() - 2.5
            if testNum == 1:
                dataFile.write(f"{x1} {1.5*x1}\n")
            elif testNum == 2:
                x2 = (SAMPLES_RANGE/2)*random.random() - 2.5
                dataFile.write(f"{x1} {x2} {3*x1 + 2*x2 + 5}\n")
            elif testNum == 3:
                dataFile.write(f"{x1} {x1**2}\n")
            elif testNum == 4:
                x2 = (SAMPLES_RANGE/2)*random.random() - 2.5
                dataFile.write(f"{x1} {x2} {5*x1+2*x2**2}\n")
        return [fileName, inputSize, outputSize]

def clear_data(test_num):
    user_input = input("\nDelete generated data files? [y/n] ")
    while user_input not in ['y', 'n']:
        user_input = input("Wrong input. [y/n] ")
    if user_input == 'y':
        for iter in range(1, test_num + 1):
            try:
                os.remove(f"data{iter}")
            except Exception as e:
                print(f"Failed to delete data{iter}. error: {e}")

for cur_test in range(1,5):
    print(f"test {cur_test}")
    training_set, inputSize, outputSize = generate_data(cur_test)
    #validation_set, _, _ = generate_data(cur_test)
    test_set, _, _ = generate_data(cur_test)
    cmd_line = ["python3", "training_neural_network.py", training_set, test_set, str(inputSize), str(outputSize), str(EPOCHES)]
    min_error = float('inf')
    for learning_rate in LEARNING_RATES:
        cur_cmd = cmd_line + [str(learning_rate), str(HIDDEN_LAYER_SIZE)]
        process = subprocess.run(cur_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        print(f"error in test 1\n{process.stderr}") if process.returncode != 0 else None
        cur_error = float(process.stdout.split()[-1])
        if cur_error < min_error:
            best_rate = learning_rate
            min_error = cur_error
    error_precent = 100*min_error/(SAMPLES_RANGE/2)
    print(f"Best learning rate: {best_rate}, with mean error: {error_precent}%") if min_error != float('inf') else None

clear_data(cur_test)
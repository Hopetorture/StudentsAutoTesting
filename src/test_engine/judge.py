#!/usr/bin/python
import argparse
import subprocess
import json

from subprocess import CalledProcessError
from multiprocessing import Pool

PROC_COUNT = 8


class TestResult:
    def __init__(self, status, message):
        self.status = status
        self.message = message


def compile_cpp(code):
    with open('main.cpp', 'w') as file:
        file.write(code)

    try:
        results = subprocess.check_output(['g++', 'main.cpp', '-Wall', '-fpermissive'],
                                          stderr=subprocess.STDOUT).decode('utf-8')
    except CalledProcessError as e:
        results = e.output.decode('utf-8')

    return results


def run_cpp(input):
    try:
        runtime_results = subprocess.check_output(['./a.out'] + input['Stdin_input'],
                                                  stderr=subprocess.STDOUT).decode('utf-8')
    except CalledProcessError as e:
        runtime_results = e.output.decode('utf-8')
    except FileNotFoundError as e:
        runtime_results = 'Not compiled'
    return runtime_results


TOOLCHAINS = {
    'g++': (compile_cpp, run_cpp)
}


# scrap this idea for now due to problems - each executable must have its own input.txt.
# it can be solved by copying binary to a special directory tree to make a match between run and a testcase input txt
# def write_inputtxt(testcases):
#     for k,v in testcases.items():
#         with open('input.txt', 'w') as f:
#             f.write(file_data)

def judge(task_json, question):
    question = json.loads(question)
    task = json.loads(task_json)
    compile_fn, run_fn = TOOLCHAINS[task['Toolkit']]
    compile_result = compile_fn(code=task['Code'])
    if compile_result:
        # report an error here, coz we got a compilation error/warning
        if 'error' in compile_result:
            print('Could not compile!')
            print(compile_result)
            return


    pool = Pool(len(question['testcases']) % PROC_COUNT)
    #pool = Pool(1)
    runtime_results = pool.map(run_fn, question['testcases'])

    test_results = {}
    for i in range(len(runtime_results)):
        correct_answer = question['testcases'][i]['Output_value']
        runtime_answer = runtime_results[i]
        if correct_answer != runtime_answer:
            if (runtime_answer.replace(' ', '').replace('\n', '') ==
                    correct_answer.replace(' ', '').replace('\n', '')):
                # fuzzy compare is OK, mb formatting error.
                test_results[i] = TestResult(
                    'Fail', 'Wrong answer. Possible formatting mismatch.')
            else:
                test_results[i] = TestResult('Fail', 'Wrong answer')
        else:
            test_results[i] = TestResult('Success', 'Correct answer')

    print(compile_result + '\n')
    for k, v in test_results.items():
        print('Testcase #{id}: {res}, {msg}'.format(
            id=k, res=v.status, msg=v.message))
    print('1')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", type=str, help="input json for a task")
    parser.add_argument("-q", type=str, help="question json")
    args = parser.parse_args()
    judge(args.t, args.q)


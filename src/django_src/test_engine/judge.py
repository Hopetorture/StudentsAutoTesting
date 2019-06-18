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


def run_cpp(input, timeout=3):
    try:
        runtime_results = subprocess.check_output(['./a.out'] + input['Stdin_input'],
                                                  stderr=subprocess.STDOUT, timeout=timeout).decode('utf-8')
    except CalledProcessError as e:
        runtime_results = e.output.decode('utf-8')
    except FileNotFoundError as e:
        runtime_results = 'Not compiled'
    except subprocess.TimeoutExpired:
        runtime_results = 'Execution timeout'
    return runtime_results


TOOLCHAINS = {
    'C++14': (compile_cpp, run_cpp)
}


def fail_to_bool(s):
    if 'Success' in s:
        return True
    else:
        return False

def parse_jsons(js):
    try:
        return json.loads(js)
    except TypeError:
        return js


def judge(task_json, question):
    question = parse_jsons(question)
    task = parse_jsons(task_json)
    if not question['testcases']:
        print(json.dumps(ResultTemplate.standart_res('')))
        return
    compile_fn, run_fn = TOOLCHAINS[task['Toolkit']]
    compile_result = compile_fn(code=task['Code'])
    if compile_result:
        if 'error' in compile_result:
            #print('Could not compile!')
            #print(compile_result)
            print(json.dumps(ResultTemplate.compile_error(compile_result)))
            return

    pool = Pool(max(len(question['testcases']) % PROC_COUNT, 1))
    #pool = Pool(1)
    runtime_results = pool.map(run_fn, question['testcases'])
    test_results = {}
    for i in range(len(runtime_results)):
        correct_answer = question['testcases'][i]['Output_value'].replace('\\n', '\n')
        runtime_answer = runtime_results[i]
        #print('RUNTIME ANSWER:')
        #print(runtime_answer)
        if 'Execution timeout' in runtime_answer:
            compile_result = f'Timeout in test {i}'
        if correct_answer != runtime_answer:
            if (runtime_answer.replace(' ', '').replace('\n', '') ==
                    correct_answer.replace(' ', '').replace('\n', '')):
                # fuzzy compare is OK, mb formatting error.
                test_results[i] = TestResult('Success', 'Correct answer')
            else:
                test_results[i] = TestResult('Fail', 'Wrong answer')
        else:
            test_results[i] = TestResult('Success', 'Correct answer')

    tests_status = 'Success'
    result_json = ResultTemplate.standart_res(compile_result)
    # print(compile_result + '\n')
    for k, v in test_results.items():
        result_json['testcase_status'].append({
                'idx': k,
                'status': v.status,
                'bool_stat': fail_to_bool(v.status)
            })
        if v.status == 'Fail':
            tests_status = 'Fail'
        #print('Testcase #{id}: {res}, {msg}'.format(
        #    id=k, res=v.status, msg=v.message))
    result_json['status'] = tests_status
    result_json['color'] = get_color_for_status(tests_status)
    print(json.dumps(result_json))


class ResultTemplate:
    @staticmethod
    def compile_error(err):
        return {
            'compile_result': err,
            'testcase_status': [],
            'status': 'Not compiled',
            'color': 'Brass'
        }
    @staticmethod
    def standart_res(compile_result):
        return {
            'compile_result': compile_result,
            'testcase_status': [],
            'status': 'Success',
            'color': 'black'
        }


def get_color_for_status(status):
    if 'Success' in status:
        return 'green'
    elif 'Fail' in status:
        return 'red'
    elif 'Not compiled' in status:
        return 'Brass'
    else:
        return 'black'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", type=str, help="input json for a task")
    parser.add_argument("-q", type=str, help="question json")
    args = parser.parse_args()
    judge(args.t, args.q)


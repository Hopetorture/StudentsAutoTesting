#!/usr/bin/python3
import subprocess
import json

d1 = {
    "Type": "CodeQuestion",

    "Code": str('''#include <iostream>

using namespace std;

int main(int argc, char** argv)
{
    int summ = 0;
    for(int i = 1; i < argc; i++){
        summ += atoi(argv[i]);
     }
    cout << summ;
    return 0;
}'''),
    "JobID": "9",
    "UserID": "13",
    "QuestionID": "42",
    "Toolkit": "g++"
}

d2 = {"QuestionID": "42",
      "Title": "str",
      "Text": "text of question",
      "Timeout": "3",
      "testcases":
          [{
              "Test_id": "1",
              "Stdin_input": ["3", "3"],
              "Filestring json": "formatted string with test data input",
              "Output_type": "int",
              "Output_value": "6"
           },
              {
                  "Test_id": "2",
                  "Stdin_input": ["5", "7"],
                  "Filestring json": "tbd",
                  "Output_type": "int",
                  "Output_value": "12"
              }
          ]
      }


def run_docker(question, task):  # question = d2, t = d1
    print('docker start')
    try:
        res = subprocess.check_output(["docker", "run", "test-engine", "-q", json.dumps(question), '-t', json.dumps(task)],
                       timeout=3)
    except TimeoutError as e:
        return {
            'compile_result': e,
            'testcase_status': [],
            'status': 'Fail',
            'color': 'Brass'
        }
    except subprocess.CalledProcessError as e:
        return {
            'compile_result': e,
            'testcase_status': [],
            'status': 'Fail',
            'color': 'red'
        }

    return json.loads(res.decode('utf-8').strip())


def start_for_debug():
    #from src.test_engine.judge import judge
    from . import judge
    judge(json.dumps(d1), json.dumps(d2))


if __name__ == '__main__':
    start_for_debug()
    #run_docker()

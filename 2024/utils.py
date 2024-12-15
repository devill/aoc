import sys
import os
import glob

def data_files_for(current_file):
    default_id = ''.join(filter(str.isdigit, current_file))

    if len(sys.argv) != 2:
        test_file = f'test{default_id}.txt'
        print("\n\n### Test Data ###")
        if os.path.exists(test_file):
            with open(test_file) as file:
                yield file, 'test'
        else:
            test_files = glob.glob(f'test{default_id}_*.txt')
            if test_files:
                for test_file in test_files:
                    with open(test_file) as file:
                        yield file, 'test'

        print("\n\n### Real Data ###")
        with open(f'input{default_id}.txt') as file:
            yield file, 'real'

    else:
        yield sys.argv[1]
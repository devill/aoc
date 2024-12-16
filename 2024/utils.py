import sys
import os
import glob


def data_files_for(current_file):
    default_id = ''.join(filter(str.isdigit, current_file))

    if len(sys.argv) != 2:
        test_file = f'test{default_id}.txt'
        if os.path.exists(test_file):
            print("\n\n### Test Data ###")
            with open(test_file) as file:
                yield file, {"type": 'test', "sequence_id": None}
        else:
            test_files = glob.glob(f'test{default_id}_*.txt')
            if test_files:
                for test_file in test_files:
                    sequence_id = test_file.split('_')[-1].split('.')[0]
                    print(f"\n\n### Test Data {sequence_id} ###")
                    with open(test_file) as file:
                        yield file, {"type": 'test', "sequence_id": sequence_id}

        print("\n\n### Real Data ###")
        with open(f'input{default_id}.txt') as file:
            yield file, {"type": 'real', "sequence_id": None}

    else:
        yield sys.argv[1]

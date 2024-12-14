import sys

def data_files_for(current_file):
    default_id = ''.join(filter(str.isdigit, current_file))

    if len(sys.argv) != 2:
        print("\n\n### Test Data ###")
        with open(f'test{default_id}.txt') as file:
            yield file, 'test'

        print("\n\n### Real Data ###")
        with open(f'input{default_id}.txt') as file:
            yield file, 'real'

    else:
        yield sys.argv[1]
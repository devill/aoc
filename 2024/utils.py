import sys

def data_files_for(current_file):
    default_id = ''.join(filter(str.isdigit, current_file))

    if len(sys.argv) != 2:
        print("\n\n### Test Data ###")
        yield f'test{default_id}.txt'

        print("\n\n### Real Data ###")
        yield f'input{default_id}.txt'

    else:
        yield sys.argv[1]
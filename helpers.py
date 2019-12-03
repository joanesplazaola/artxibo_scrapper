def get_last_number(files):
    values = []
    for file in files:
        with open(f'{file}.csv', 'r') as f:
            opened_file = f.readlines()
            if opened_file:
                var = opened_file[-1].split('|')[0]
                values.append(int(var))

    if values:
        init = max(values) + 1
    else:
        init = 1
    return init

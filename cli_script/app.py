cfg_string = ['/configure']


def rm_insignificant_lines(in_cfg):
    """
    Remove insignificant lines from input config file.
    These lines are starting with '#' or 'echo'
    :param in_cfg: cfg as a multiline string
    :return: cleanified array of config lines
    """
    cfg_arr = in_cfg.splitlines()
    for line in list(cfg_arr):
        if not is_cfg_statement(line):
            cfg_arr.remove(line)
    return cfg_arr


def is_cfg_statement(line):
    # if line.strip() in ['', 'exit all', 'configure'] or line.lstrip()[0] == "#" or line.lstrip()[0:4] == "echo":
    if line.strip() == '' or line[0:4] != '    ':
        return False
    else:
        return True


def rootify(clean_cfg):
    prev_ind_level = 0
    # next_ind_level = 0
    for i, line in enumerate(clean_cfg):
        if line.strip() == 'exit':
            cfg_string.pop()
            prev_ind_level -= 4
            continue

        cur_ind_level = len(line) - len(line.lstrip())
        if cur_ind_level > prev_ind_level:
            cfg_string.append(line.strip())
        elif cur_ind_level == prev_ind_level:
            cfg_string.pop()
            cfg_string.append(line.strip())
        prev_ind_level = cur_ind_level
        if i < len(clean_cfg)-1:
            next_ind_level = len(clean_cfg[i + 1]) - len(clean_cfg[i + 1].lstrip())
            if next_ind_level > prev_ind_level:
                continue
            else:
                print(' '.join(cfg_string))
        else:
            print(' '.join(cfg_string))

    return 0


with open('test_cfg.txt', 'r') as cfg:
    clean_arr = rm_insignificant_lines(cfg.read())
    rootified = rootify(clean_arr)

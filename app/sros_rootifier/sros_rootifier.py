import re
from flask import render_template, request, Blueprint, jsonify





def rm_insignificant_lines(in_cfg):
    """
    Remove insignificant lines from input config file.
    These lines are starting with '#' or 'echo'
    :param in_cfg: cfg as a multiline string
    :return: cleanified array of config lines
    """
    cfg_arr = in_cfg.splitlines()
    # make a dup array for in-place deletion
    for line in list(cfg_arr):
        if not is_cfg_statement(line):
            cfg_arr.remove(line)
    return cfg_arr


def is_cfg_statement(line):
    # if line is empty, or first for elemets are not spaces
    # consider this line for deletion
    if line.strip() == '' or line[0:4] != '    ':
        return False
    else:
        return True


def rootify(clean_cfg):
    cfg_string = ['/configure']
    rootified_cfg = """"""
    # init previous indent level as 0 for /configure line
    prev_ind_level = 0

    for i, line in enumerate(clean_cfg):
        if line.strip() == 'exit':
            cfg_string.pop()
            prev_ind_level -= 4
            continue

        # calc current indent
        cur_ind_level = len(line) - len(line.lstrip())
        # append a command if it is on a next level of indent
        if cur_ind_level > prev_ind_level:
            cfg_string.append(line.strip())
        # if a command on the same level of indent
        # we delete the prev. command and append the new one to the base string
        elif cur_ind_level == prev_ind_level:
            cfg_string.pop()
            # removing (if any) `customer xxx create` or `create` at the end of the line
            # since it was previously printed out
            cfg_string[-1] = re.sub('\scustomer\s\d+\screate$|\screate$','', cfg_string[-1])
            cfg_string.append(line.strip())

        prev_ind_level = cur_ind_level

        ## if we have a next line go check it's indent value
        if i < len(clean_cfg)-1:
            next_ind_level = len(clean_cfg[i + 1]) - len(clean_cfg[i + 1].lstrip())
            # if a next ind level is depper (>) then we can continue accumulation
            # of the commands
            if next_ind_level > prev_ind_level:
                continue
            # if the next level is the same or lower, we must save a line
            else:
                rootified_cfg += ' '.join(cfg_string) + '\n'
        else:
            # otherwise we have a last line here, so print it
            rootified_cfg += ' '.join(cfg_string) + '\n'

    return rootified_cfg




###############
#### FLASK ####
###############

sros_rootifier_bp = Blueprint('sros_rootifier', __name__, template_folder='templates', static_folder='static',
                              static_url_path='/sros_rootifier/static')


@sros_rootifier_bp.route('/sros_rootifier', methods=['GET', 'POST'])
def sros_rootifier():
    if request.method == 'GET':
        return render_template('sros_rootifier.html')

    # handle POST method from JQuery (will be filled later)
    elif request.method == 'POST':
        result = {'output_data': '',
                  'error': ''}
        input_cfg = request.form['cfg']
        clean_cfg = rm_insignificant_lines(input_cfg)
        result['output_data'] = rootify(clean_cfg)
        return jsonify(result)

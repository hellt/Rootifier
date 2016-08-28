from flask import render_template, request, Blueprint, jsonify





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
    if line.strip() == '' or line[0:4] != '    ':
        return False
    else:
        return True


def rootify(clean_cfg):
    cfg_string = ['/configure']
    rootified_cfg = """"""
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

        ## if we have a next line go check it's indent value
        if i < len(clean_cfg)-1:
            next_ind_level = len(clean_cfg[i + 1]) - len(clean_cfg[i + 1].lstrip())
            if next_ind_level > prev_ind_level:
                continue
            else:
                rootified_cfg += ' '.join(cfg_string) + '\n'
        else:
            # otherwise we have a last line here, so print it
            rootified_cfg += ' '.join(cfg_string) + '\n'
    return rootified_cfg




###############
#### FLASK ####
###############

conf_rootifier_bp = Blueprint('conf_rootifier', __name__, template_folder='templates', static_folder='static',
                              static_url_path='/cfg_rootifier/static')


@conf_rootifier_bp.route('/config_rootifier', methods=['GET', 'POST'])
def conf_rootifier():
    if request.method == 'GET':
        return render_template('conf_rootifier.html')

    # handle POST method from JQuery (will be filled later)
    elif request.method == 'POST':
        result = {'output_data': '',
                  'error': ''}
        input_cfg = request.form['cfg']
        clean_cfg = rm_insignificant_lines(input_cfg)
        result['output_data'] = rootify(clean_cfg)
        return jsonify(result)

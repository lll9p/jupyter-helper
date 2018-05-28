import io
import nbformat
def run_notebook(nbfile, **kwargs):
    """
    example:
    run_notebook('report.ipynb', platform='google_play', start_date='2016-06-10')
    """

    def read_notebook(nbfile):
        if not nbfile.endswith('.ipynb'):
            nbfile += '.ipynb'

        with io.open(nbfile) as f:
            nb = nbformat.read(f, as_version=4)
        return nb

    ip = get_ipython()
    gl = ip.ns_table['user_global']
    gl['params'] = None
    arguments_in_original_state = True

    for cell in read_notebook(nbfile).cells:
        if cell.cell_type != 'code':
            continue
        ip.run_cell(cell.source)

        if arguments_in_original_state and type(gl['params']) == dict:
            gl['params'].update(kwargs)
            arguments_in_original_state = False

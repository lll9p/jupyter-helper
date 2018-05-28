def align_figures():
    import matplotlib
    from matplotlib._pylab_helpers import Gcf
    from IPython.display import display_html
    import base64
    from ipykernel.pylab.backend_inline import show

    images = []
    for figure_manager in Gcf.get_all_fig_managers():
        fig = figure_manager.canvas.figure
        png = get_ipython().display_formatter.format(fig)[0]['image/png']
        src = base64.encodebytes(png).decode()
        images.append('<img style="margin:0" align="left" src="data:image/png;base64,{}"/>'.format(src))

    html = "<div>{}</div>".format("".join(images))
    show._draw_called = False
    matplotlib.pyplot.close('all')
    display_html(html, raw=True)

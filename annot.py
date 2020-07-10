def update_annot(ind, line, annot, ydata, datax):
    x, y = line.get_data()
    annot.xy = (x[ind["ind"][0]], y[ind["ind"][0]])
    # Get x and y values, then format them to be displayed
    x_values = datax[int(list(map(str, ind["ind"]))[0])]
    y_values = " ".join(str(ydata[n]) for n in ind["ind"]).split(' ')[0]
    text = "{}: {}".format(x_values, y_values)
    annot.set_text(text)
    annot.get_bbox_patch().set_alpha(1.0)

def hover(event, line_info, fig, ax, datax):
    line, annot, ydata = line_info
    vis = annot.get_visible()
    if event.inaxes == ax:
        # Draw annotations if cursor in right position
        cont, ind = line.contains(event)
        if cont:
            update_annot(ind, line, annot, ydata, datax)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            # Don't draw annotations
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

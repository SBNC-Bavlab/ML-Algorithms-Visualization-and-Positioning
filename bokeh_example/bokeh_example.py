from bokeh.models.annotations import Arrow
from bokeh.plotting import figure
from bokeh.models.arrow_heads import OpenHead, NormalHead, VeeHead
from bokeh.io import output_notebook, show


p = figure(plot_width=600, plot_height=600)

#p.axis.visible = False
#p.toolbar.logo = None
#p.toolbar_location = None
#p.xgrid.grid_line_color = None
#p.ygrid.grid_line_color = None

space_offset = 2

x_offset = 10 + space_offset
y_offset = 20

root_x = 0
root_y = 20

ellipse_width = 10
ellipse_height = 5

x_coordinates = [
                 root_x,
                 root_x + 0*x_offset,
                 root_x + 1*x_offset,
                 root_x + 2*x_offset,
                 root_x
                ]

y_coordinates = [
                 root_y,
                 root_y - y_offset,
                 root_y - y_offset,
                 root_y - y_offset,
                 root_y - 2*y_offset
                ]

colors = ["blue", "green", "yellow", "red", "brown"]

texts = ["test", "test", "test", "test", "test"]

p.ellipse(x_coordinates, y_coordinates, width=ellipse_width, height=ellipse_height,
         color=colors, fill_alpha=0.1)

p.text(x_coordinates, y_coordinates, text=texts)

for i in range(len(x_coordinates[1:])):
    p.add_layout(Arrow(
                   line_width = 0.5,
                   end = OpenHead(line_width=0.5),
                   x_start = root_x,
                   y_start = root_y - ellipse_height/2,
                   x_end = x_coordinates[i+1],
                   y_end = y_coordinates[i+1] + ellipse_height/2
                  )
            )

show(p)

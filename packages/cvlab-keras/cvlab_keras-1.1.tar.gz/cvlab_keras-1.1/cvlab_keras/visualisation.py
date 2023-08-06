import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from cvlab.diagram.elements.base import *
from .model_utils import model_to_image
from .shared import PLUGIN_PRIORITY


matplotlib.use('Qt5Agg')


class Graph(FigureCanvasQTAgg):

    def __init__(self,  name, width, height, dpi):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.name = name
        super(Graph, self).__init__(self.figure)

    def live_plotter(self, x_vec, y_vec):
        pass

    def draw_figure(self):
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        data = np.fromstring(self.figure.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        data = data.reshape(self.figure.canvas.get_width_height()[::-1] + (3,))
        return data

    def set_ax(self, line, ax, x_vec, y_vec):
        line.set_xdata(x_vec)
        line.set_ydata(y_vec)
        ax.relim()
        ax.autoscale_view()

    def configure(self, ax, title, y_label, x_label="Batch"):
        ax.set_autoscaley_on(True)
        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)


class SingleGraph(Graph):

    def __init__(self, name, width=5, height=4, dpi=100):
        super().__init__(name, width, height, dpi)
        self.ax = self.figure.add_subplot(111)
        self.line, = self.ax.plot([], [], linewidth=0.5)
        self.title = name + " function"
        self.configure(self.ax, self.title, self.name)

    def live_plotter(self, x_vec, y_vec):
        self.set_ax(self.line, self.ax, x_vec, y_vec)
        return self.draw_figure()


class MultiGraph(Graph):

    def __init__(self, name, width=5, height=4, dpi=100):
        super().__init__(name, width, height, dpi)
        self.ax = list()
        self.ax.append(self.figure.add_subplot(211))
        self.ax.append(self.figure.add_subplot(212))
        self.figure.tight_layout(pad=4.0)
        self.line = list()
        for a in self.ax:
            tmp, = a.plot([], [], lw=0.5)
            self.line.append(tmp)
        self.title = [n + " function" for n in self.name]
        self.configure_plots()

    def configure_plots(self):
        for i in range(len(self.ax)):
            super().configure(self.ax[i], self.title[i], self.name[i])

    def live_plotter(self, x_vec, y_vec):
        for i in range(len(self.line)):
            self.set_ax(self.line[i], self.ax[i], x_vec, y_vec[i])
        return self.draw_figure()


class MetricsPlotter(NormalElement):
    name = "Metrics plotter"
    comment = """\
    Generates plots for different metrics functions in real time.
    
    Loss - loss function
    Accuracy - accuracy function
    All - loss and accuracy functions in one figure 
    Batch step - number of batches to refresh data in the chart"""

    LOSS = 0
    ACCURACY = 1
    ALL = 2

    def __init__(self):
        super(MetricsPlotter, self).__init__()

        self.counter = 0
        self.loss = []
        self.accuracy = []
        self.batch_num = []
        self.img = []
        self.diagrams = []
        self.toolbars = []
        self.combo_param = ""
        self.input_param = {}
        self.widget_stack_fig = QStackedWidget()
        self.widget_stack_bar = QStackedWidget()

        self.set_all_diagrams()

    def set_all_diagrams(self):
        self.create_diagram(self.LOSS, "Loss")
        self.create_diagram(self.ACCURACY, "Accuracy")
        self.create_diagram(self.ALL, ["Loss", "Accuracy"])

        self.layout().addWidget(self.widget_stack_bar)
        self.layout().addWidget(self.widget_stack_fig)

    def create_diagram(self, type, name):
        if type != self.ALL:
            self.diagrams.insert(type, SingleGraph(name))
        else:
            self.diagrams.insert(type, MultiGraph(name))
        self.widget_stack_fig.addWidget(self.diagrams[type])
        self.toolbars.insert(type, NavigationToolbar(self.diagrams[type], self))
        self.widget_stack_bar.addWidget(self.toolbars[type])

    def get_attributes(self):
        return [Input("metrics")], \
               [Output("image")], \
               [IntParameter("batch_step", value=1, min_=1),
                ComboboxParameter("function", {"Loss": "loss", "Accuracy": "acc", "All": "all"})]

    def process_inputs(self, inputs, outputs, parameters):
        model_data = inputs["metrics"].value
        if model_data != self.input_param:
            self.input_param = model_data
            self.loss.append(model_data["loss"])
            self.accuracy.append(model_data["accuracy"])
            self.counter += 1
            self.batch_num.append(self.counter)

        batch_step = parameters["batch_step"]
        func = parameters["function"]
        if self.counter % batch_step == 0 or func != self.combo_param:
            self.combo_param = func
            self.choose_param(func)

        outputs["image"] = Data(self.img)

    def choose_param(self, func):
        if func == "loss":
            self.print_result(self.LOSS)
        elif func == "acc":
            self.print_result(self.ACCURACY)
        elif func == "all":
            self.print_result(self.ALL)

    def print_result(self, type):
        self.widget_stack_bar.setCurrentWidget(self.toolbars[type])
        self.widget_stack_fig.setCurrentWidget(self.diagrams[type])
        self.img = self.diagrams[type].live_plotter(self.batch_num, self.list_type(type))

    def list_type(self, type):
        if type == self.LOSS:
            return self.loss
        elif type == self.ACCURACY:
            return self.accuracy
        elif type == self.ALL:
            return [self.loss, self.accuracy]


class ModelToImage(NormalElement):
    name = 'Model to image'
    comment = 'Plots model to graphical representation\n' \
              'Requires Pydot module to work'

    def get_attributes(self):
        return [Input("model")], [Output("image")], []

    def process_inputs(self, inputs, outputs, parameters):
        model = inputs["model"].value

        image = model_to_image(model)
        self.outputs["image"].put(Data(image))


register_elements_auto(__name__, locals(), "Keras visualisation", PLUGIN_PRIORITY + 4)

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .networks import all_depth_first_branches, get_branch_points, reduce_branch
import numpy as np, math
from .morphologies import Compartment
from contextlib import contextmanager


class CellTrace:
    def __init__(self, meta, data):
        self.meta = meta
        self.data = data


class CellTraces:
    def __init__(self, id, title):
        self.traces = []
        self.cell_id = id
        self.title = title

    def add(self, meta, data):
        self.traces.append(CellTrace(meta, data))

    def __iter__(self):
        return iter(self.traces)

    def __len__(self):
        return len(self.traces)


class CellTraceCollection:
    def __init__(self, cells=None):
        if cells is None:
            cells = {}
        elif isinstance(cells, list):
            cells = dict(map(lambda cell: (cell.cell_id, cell), cells))
        self.cells = cells
        self.legends = []
        self.colors = []

    def set_legends(self, legends):
        self.legends = legends

    def set_colors(self, colors):
        self.colors = colors

    def add(self, id, meta, data):
        if not id in self.cells:
            self.cells[id] = CellTraces(id, meta["display_label"])
        self.cells[id].add(meta, data)

    def __iter__(self):
        return iter(self.cells.values())

    def __len__(self):
        return len(self.cells)


@contextmanager
def show_network_figure(fig=None, cubic=True, show=True, legend=True, swapaxes=True):
    try:
        if fig is None:
            fig = go.Figure()
        yield fig
    finally:
        fig.update_layout(scene=dict(xaxis_title="x", yaxis_title="z", zaxis_title="y"))
        fig.update_layout(showlegend=legend)
        if cubic:
            fig.update_layout(scene_aspectmode="cube")
        if swapaxes:
            fig.update_layout(
                scene=dict(xaxis_title="X", yaxis_title="Z", zaxis_title="Y")
            )
        if show:
            fig.show()


def plot_network(scaffold, from_memory=True, show=True):
    if from_memory:
        with show_network_figure(show=show) as fig:
            for type in scaffold.configuration.cell_types.values():
                if type.entity:
                    continue
                pos = scaffold.cells_by_type[type.name][:, [2, 3, 4]]
                color = type.plotting.color
                fig.add_trace(
                    go.Scatter3d(
                        x=pos[:, 0],
                        y=pos[:, 2],
                        z=pos[:, 1],
                        mode="markers",
                        marker=dict(color=color, size=type.placement.radius),
                        opacity=type.plotting.opacity,
                        name=type.plotting.label,
                    )
                )
            return fig
    else:
        scaffold.reset_network_cache()
        for type in scaffold.configuration.cell_types.values():
            if type.entity:
                continue
            # Load from HDF5
            scaffold.get_cells_by_type(type.name)
        plot_network(scaffold, from_memory=True, show=show)


def plot_detailed_network(scaffold, ids=None, show=True):
    from .output import MorphologyRepository

    with show_network_figure(show=show, legend=False) as fig:
        ms = MorphologyScene(fig)
        mr = scaffold.morphology_repository

        for cell_type in scaffold.configuration.cell_types.values():
            segment_radius = 1.0
            if cell_type.name != "granule_cell":
                segment_radius = 2.5
            m_names = cell_type.list_all_morphologies()
            if len(m_names) == 0:
                continue
            if len(m_names) > 1:
                raise NotImplementedError(
                    "We haven't implemented plotting different morphologies per cell type yet. Open an issue if you need it"
                )
            cells = scaffold.get_placement_set(cell_type.name).cells
            morpho = mr.get_morphology(m_names[0])
            for cell in cells:
                if ids is not None and cell.id not in ids:
                    continue
                ms.add_morphology(
                    morpho,
                    cell.position,
                    color=cell_type.plotting.color,
                    soma_radius=cell_type.placement.soma_radius,
                    segment_radius=segment_radius,
                )
        ms.prepare_plot()
        scene = fig.layout.scene
        scene.xaxis.range = [-200, 200]
        scene.yaxis.range = [-200, 200]
        scene.zaxis.range = [0, 600]


def get_voxel_cloud_traces(cloud, selected_voxels=None, offset=[0.0, 0.0, 0.0]):
    # Calculate the 3D voxel indices based on the voxel positions and the grid size.
    boxes = cloud.get_boxes()
    voxels = cloud.voxels.copy()
    box_positions = np.column_stack(boxes[:, voxels])
    # Calculate normalized occupancy of each voxel to determine transparency
    occupancies = cloud.get_occupancies() / 1.5

    colors = np.empty(voxels.shape, dtype=object)
    if selected_voxels is not None:
        # Color selected voxels
        colors[voxels] = "rgba(0, 0, 0, 0.0)"
        colors[selected_voxels] = "rgba(0, 255, 0, 1.0)"
    else:
        # Prepare voxels with the compartment density coded into the alpha of the facecolor
        colors[voxels] = list(map(lambda o: "rgba(255, 0, 0, {})".format(o), occupancies))
    traces = []
    for box, color in zip(box_positions, colors[voxels]):
        box += offset
        traces.extend(
            plotly_block(box, [cloud.grid_size, cloud.grid_size, cloud.grid_size], color)
        )

    return traces


def plot_voxel_cloud(
    cloud, bounds, selected_voxels=None, fig=None, show=True, offset=[0.0, 0.0, 0.0]
):
    with show_network_figure(legend=False, fig=fig, show=show) as fig:
        traces = get_voxel_cloud_traces(
            cloud, selected_voxels=selected_voxels, offset=offset
        )
        for trace in traces:
            fig.add_trace(trace)
        # set_scene_range(fig.layout.scene, bounds)
        return fig


def get_branch_trace(compartments, offset=[0.0, 0.0, 0.0], color="black", width=1.0):
    x = [c.start[0] + offset[0] for c in compartments]
    y = [c.start[1] + offset[1] for c in compartments]
    z = [c.start[2] + offset[2] for c in compartments]
    # Add branch endpoint
    x.append(compartments[-1].end[0] + offset[0])
    y.append(compartments[-1].end[1] + offset[1])
    z.append(compartments[-1].end[2] + offset[2])
    return go.Scatter3d(x=x, y=z, z=y, mode="lines", line=dict(width=width, color=color))


def get_soma_trace(soma_radius, offset=[0.0, 0.0, 0.0], color="black"):
    theta = np.linspace(0, 2 * np.pi, 10)
    phi = np.linspace(0, np.pi, 10)
    x = np.outer(np.cos(theta), np.sin(phi)) * soma_radius + offset[0]
    y = np.outer(np.sin(theta), np.sin(phi)) * soma_radius + offset[2]
    z = np.outer(np.ones(10), np.cos(phi)) * soma_radius + offset[1]
    return go.Surface(
        x=x,
        y=y,
        z=z,
        surfacecolor=np.zeros(10),
        colorscale=[[0, color], [1, color]],
        showscale=False,
    )


def plot_morphology(
    morphology,
    return_traces=False,
    offset=[0.0, 0.0, 0.0],
    fig=None,
    show=True,
    set_range=True,
    color="black",
    reduce_branches=False,
    soma_radius=None,
    segment_radius=1.0,
):
    compartments = np.array(morphology.compartments.copy())
    dfs_list = all_depth_first_branches(morphology.get_compartment_network())
    if reduce_branches:
        branch_points = get_branch_points(dfs_list)
        dfs_list = list(map(lambda b: reduce_branch(b, branch_points), dfs_list))
    traces = []
    for branch in dfs_list[::-1]:
        traces.append(
            get_branch_trace(
                compartments[branch], offset, color=color, width=segment_radius
            )
        )
    traces.append(
        get_soma_trace(
            soma_radius if soma_radius is not None else compartments[0].radius,
            offset,
            color,
        )
    )
    if return_traces:
        return traces
    else:
        if fig is None:
            fig = go.Figure()
            fig.update_layout(showlegend=False)
        for trace in traces:
            fig.add_trace(trace)
        if set_range:
            set_scene_range(fig.layout.scene, morphology.get_plot_range(offset=offset))
        if show:
            fig.show()
        return fig


def plot_intersections(
    from_morphology,
    from_pos,
    to_morphology,
    to_pos,
    intersections,
    offset=[0.0, 0.0, 0.0],
    fig=None,
):
    from_compartments = (
        np.array(from_morphology.compartment_tree.get_arrays()[0])
        + np.array(offset)
        + np.array(from_pos)
    )
    to_compartments = (
        np.array(to_morphology.compartment_tree.get_arrays()[0])
        + np.array(offset)
        + np.array(to_pos)
    )
    if fig is None:
        fig = go.Figure()
        fig.update_layout(showlegend=False)
        fig.show()


def plot_block(fig, origin, sizes, color=None, colorscale="Cividis", **kwargs):
    edges, faces = plotly_block(origin, sizes, color, colorscale)
    # fig.add_trace(edges, **kwargs)
    fig.add_trace(faces, **kwargs)


def plotly_block(origin, sizes, color=None, colorscale_value=None, colorscale="Cividis"):
    return plotly_block_edges(origin, sizes), plotly_block_faces(origin, sizes, color)


def plotly_block_faces(
    origin,
    sizes,
    color=None,
    colorscale_value=None,
    colorscale="Cividis",
    cmin=0,
    cmax=16.0,
):
    # 8 vertices of a block
    x = origin[0] + np.array([0, 0, 1, 1, 0, 0, 1, 1]) * sizes[0]
    y = origin[1] + np.array([0, 1, 1, 0, 0, 1, 1, 0]) * sizes[1]
    z = origin[2] + np.array([0, 0, 0, 0, 1, 1, 1, 1]) * sizes[2]
    color_args = {}
    if colorscale_value:
        color_args = {
            "colorscale": colorscale,
            "intensity": np.ones((8)) * colorscale_value,
            "cmin": cmin,
            "cmax": cmax,
        }
    if color:
        color_args = {"color": color}
    return go.Mesh3d(
        x=x,
        y=z,
        z=y,
        # i, j and k give the vertices of the mesh triangles
        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        opacity=0.3,
        **color_args
    )


def plotly_block_edges(origin, sizes):
    x = origin[0] + np.array([0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]) * sizes[0]
    y = origin[1] + np.array([0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1]) * sizes[1]
    z = origin[2] + np.array([0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0]) * sizes[2]
    return go.Scatter3d(x=x, y=z, z=y, mode="lines", line=dict(width=1.0, color="black"))


def set_scene_range(scene, bounds):
    if hasattr(scene, "layout"):
        scene = scene.layout.scene  # Scene was a figure
    scene.xaxis.range = bounds[0]
    scene.yaxis.range = bounds[2]
    scene.zaxis.range = bounds[1]


def set_morphology_scene_range(scene, offset_morphologies):
    """
        Set the range on a scene containing multiple morphologies.

        :param scene: A scene of the figure. If the figure itself is given, ``figure.layout.scene`` will be used.
        :param offset_morphologies: A list of tuples where the first element is offset and the 2nd is the :class:`Morphology`
    """
    bounds = np.array(list(map(lambda m: m[1].get_plot_range(m[0]), offset_morphologies)))
    combined_bounds = np.array(
        list(zip(np.min(bounds, axis=0)[:, 0], np.max(bounds, axis=0)[:, 1]))
    )
    span = max(map(lambda b: b[1] - b[0], combined_bounds))
    combined_bounds[:, 1] = combined_bounds[:, 0] + span
    set_scene_range(scene, combined_bounds)


def hdf5_plot_spike_raster(spike_recorders):
    """
        Create a spike raster plot from an HDF5 group of spike recorders.
    """
    cell_ids = [int(k) for k in spike_recorders.keys()]
    x = {}
    y = {}
    colors = {}
    ids = {}
    for cell_id, dataset in spike_recorders.items():
        data = dataset[:, 0]
        attrs = dict(dataset.attrs)
        label = attrs["label"]
        if not label in x:
            x[label] = []
        if not label in y:
            y[label] = []
        if not label in colors:
            colors[label] = attrs["color"]
        if not label in ids:
            ids[label] = 0
        cell_id = ids[label]
        ids[label] += 1
        # Add the spike timings on the X axis.
        x[label].extend(data)
        # Set the cell id for the Y axis of each added spike timing.
        y[label].extend(cell_id for _ in range(len(data)))
    # Use the parallel arrays x & y to plot a spike raster
    fig = go.Figure(
        layout=dict(
            xaxis=dict(title_text="Time (ms)"), yaxis=dict(title_text="Cell (ID)")
        )
    )
    sort_by_size = lambda d: {k: v for k, v in sorted(d.items(), key=lambda i: len(i[1]))}
    start_id = 0
    for label, x, y in [(label, x[label], y[label]) for label in sort_by_size(x).keys()]:
        y = [yi + start_id for yi in y]
        start_id += ids[label]
        plot_spike_raster(x, y, label=label, fig=fig, show=False, color=colors[label])
    fig.show()


def plot_spike_raster(
    spike_timings, cell_ids, fig=None, show=True, label="Cells", color=None
):
    if fig is None:
        fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=spike_timings,
            y=cell_ids,
            mode="markers",
            marker=dict(symbol="square", size=4, color=color or "black"),
            name=label,
        )
    )
    if show:
        fig.show()


def hdf5_gather_voltage_traces(handle, root, groups=None):
    if groups is None:
        groups = [""]
    if len(groups) == 0:
        groups = [""]
    traces = CellTraceCollection()
    for group in groups:
        path = root + group
        for name, dataset in handle[path].items():
            meta = {}
            id = int(name.split(".")[0])
            meta["id"] = id
            meta["location"] = name
            meta["group"] = path
            for k, v in dataset.attrs.items():
                meta[k] = v
            traces.add(id, meta, dataset)
    return traces


def plot_traces(traces):
    fig = make_subplots(
        cols=1, rows=len(traces), subplot_titles=[trace.title.title() for trace in traces]
    )
    legend_groups = set()
    legends = traces.legends
    for i, cell_traces in enumerate(traces):
        for j, trace in enumerate(cell_traces):
            showlegend = legends[j] not in legend_groups
            fig.append_trace(
                go.Scatter(
                    x=trace.data[:, 0],
                    y=trace.data[:, 1],
                    legendgroup=legends[j],
                    name=legends[j],
                    showlegend=showlegend,
                    mode="lines",
                    marker=dict(color=traces.colors[j]),
                ),
                col=1,
                row=i + 1,
            )
            legend_groups.add(legends[j])
    fig.show()


class MorphologyScene:
    def __init__(self, fig=None):
        self.fig = fig or go.Figure()
        self._morphologies = []

    def add_morphology(self, morphology, offset=[0.0, 0.0, 0.0], **kwargs):
        self._morphologies.append((offset, morphology, kwargs))

    def show(self):
        self.prepare_plot()
        self.fig.show()

    def prepare_plot(self):
        if len(self._morphologies) == 0:
            raise MorphologyError("Cannot show empty MorphologyScene")
        for o, m, k in self._morphologies:
            plot_morphology(m, offset=o, show=False, fig=self.fig, **k)
        set_morphology_scene_range(self.fig.layout.scene, self._morphologies)

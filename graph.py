import networkx as nx
from bokeh.io import show
from bokeh.plotting import figure, from_networkx
from bokeh.models import Circle, HoverTool, MultiLine, TapTool, BoxSelectTool, ColumnDataSource, ImageURL

# Create a new graph
G = nx.Graph()

# Add nodes and edges
countries = ["India", "Pakistan", "Bangladesh", "Nepal", "Bhutan", "Sri Lanka", "Maldives", "Afghanistan"]
edges = [
    ("India", "Pakistan"),
    ("India", "Bangladesh"),
    ("India", "Nepal"),
    ("India", "Bhutan"),
    ("India", "Afghanistan"),
    ("Pakistan", "Afghanistan"),
    ("Nepal", "Bhutan")
]

# Add nodes using integer indices
for idx, country in enumerate(countries):
    G.add_node(idx, name=country)

# Add edges using integer indices
for edge in edges:
    G.add_edge(countries.index(edge[0]), countries.index(edge[1]))

# Position using spring layout
pos = nx.spring_layout(G)
pos = {node: list(position) for node, position in pos.items()}

# Create a Bokeh plot with adjusted dimensions
plot = figure(title="Countries Sharing Borders in South Asia", x_range=(-2.5, 2.5), y_range=(-2.5, 2.5),
             tools="pan,box_zoom,reset,save,tap,wheel_zoom", toolbar_location="above", plot_width=900, plot_height=700)

# Create a Bokeh graph from the NetworkX input using nx.spring_layout with adjusted scale
graph = from_networkx(G, pos, scale=2.5, center=(0, 0))

# Update node renderer data source to have country names and image URLs as additional columns
graph.node_renderer.data_source.data['name'] = [G.nodes[idx]['name'] for idx in G.nodes()]
graph.node_renderer.data_source.data['image'] = [f"{G.nodes[idx]['name']}.png" for idx in G.nodes()]

# Use ImageURL glyph for nodes to display images with adjusted size and anchor point
graph.node_renderer.glyph = ImageURL(url="image", w=0.2, h=0.2, anchor="center")
graph.node_renderer.selection_glyph = ImageURL(url="image", w=0.2, h=0.2, anchor="center")
graph.node_renderer.hover_glyph = ImageURL(url="image", w=0.2, h=0.2, anchor="center")

# Adjust edge line width for visibility
graph.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=2)

# Add hover tool to display country names
hover = HoverTool(tooltips=[("Country", "@name")])
plot.add_tools(hover, TapTool(), BoxSelectTool())

plot.renderers.append(graph)

# Show the plot
show(plot)

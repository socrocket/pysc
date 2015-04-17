import pydot

def create_branch(graph, node):
  for child in node.children():
    graph.add_node(pydot.Node(child.name(), label="%s : %s" % (child.basename(), child.kind())))
    graph.add_edge(pydot.Edge(node.name(), child.name()))
    create_branch(graph, child)

def to_file(top, filename):
  graph = pydot.Dot(graph_type='graph')
  graph.add_node(pydot.Node(top.name(), label="%s : %s" % (top.basename(), top.kind())))
  create_branch(graph, top)

  graph.write_svg(filename)


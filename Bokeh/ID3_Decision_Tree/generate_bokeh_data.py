from Bokeh.ID3_Decision_Tree.id3_decision_tree import generate_tree, set_active_attr
from Bokeh.ID3_Decision_Tree.bucheim import tree_layout


def get_depth(node, id_index, visited={}):
    """ Calculate depth of the tree """
    if node.decision in ["unacc", "acc", "good", "vgood", "1", "2", "3"]:
        node.name = "classAttr"

    if not node.children:
        node.depth = 1
        # node.id = str(id_index)
        visited[node] = False
        id_index += 1
        return 1

    max_depth = max([get_depth(child, id_index, visited) for child in node.children])

    # node.id = str(id_index)
    node.depth = max_depth + 1
    visited[node] = False
    id_index += 1
    return max_depth + 1


def get_width(node, level):
    """ Calculate width of the level"""
    if node is None:
        return 0
    if level == 1:
        return 1
    elif level > 1:
        if node.parentPointer:
            node.depth = node.parentPointer.depth - 1
        return sum([get_width(child, level-1) for child in node.children])


def get_max_width(node, depth):
    """ Calculate max width of the tree """
    max_width = 0
    h = depth
    level_widths = []
    for i in range(1, h+1):
        width = get_width(node, i)
        level_widths.append(width)
        if width > max_width:
            max_width = width
    return max_width, level_widths


def generate_node_list(root, visited):
    """ Push tree node to the list according to the breadth first search """
    node_list = []

    queue = [root]

    visited[root] = True

    while queue:

        popped_node = queue.pop(0)
        node_list.append(popped_node)

        for child in popped_node.children:
            if visited[child] is False:
                queue.append(child)
                visited[child] = True

    return node_list


def fill_source(source, node_list):
    """ Fill the source dictionary to pass bokeh"""
    for node in node_list:
        source["x"].append(node.coord[0])

        source["y"].append(node.coord[1])

        if node.children:
            source["nonLeafNodes_x"].append(node.coord[0])
            source["nonLeafNodes_y"].append(node.coord[1])
            source["nonLeafNodes_stat"].append(node.value)
            source["nonLeafNodes_decision"].append(node.decision)
            source["leafNodes_x"].append(None)
            source["leafNodes_y"].append(None)
        else:
            source["nonLeafNodes_x"].append(None)
            source["nonLeafNodes_y"].append(None)
            source["nonLeafNodes_stat"].append(None)
            source["nonLeafNodes_decision"].append(None)
            source["leafNodes_x"].append(node.coord[0])
            source["leafNodes_y"].append(node.coord[1])

        if node.name == "":
            source["attribute_type"].append("classAttr")
        else:
            source["attribute_type"].append(node.name)

        source["stat_value"].append(node.value)
        source["decision"].append(node.decision)
        source["instanceCount"].append(len(node.data))
        source["instances"].append(len(node.data))


def get_bokeh_data(method, active_attr_list=[], set_root_attribute=""):
    """ Generate tree, fill source dictionary and return corresponding values to the plotting functions"""
    id_index = 0
    set_active_attr(active_attr_list)
    root, acc = generate_tree(method, set_root_attribute)

    visited = {}
    depth = get_depth(root, id_index, visited)
    width, level_width = get_max_width(root, depth)

    source = {"nonLeafNodes_x": [], "nonLeafNodes_y": [], "nonLeafNodes_stat": [],
              "nonLeafNodes_decision": [], "leafNodes_x": [], "leafNodes_y": [],
              "attribute_type": [], "stat_value": [], "decision": [], "instanceCount": [],
              "instances": [], "x": [], "y": [], "treeMode": []}

    node_list = generate_node_list(root, visited)

    for node in node_list:
        if node.parentPointer:
            node.order_number = node.parentPointer.children.index(node) + 1

    tree_layout(root)

    min_width = min([node.coord[1] for node in node_list])
    if min_width < 1.0:
        padding = 1.0 - min_width

        for node in node_list:
            node.coord = (node.coord[0], node.coord[1] + padding)

    fill_source(source, node_list)
    width = max([node.coord[1] for node in node_list])
    source["treeMode"] = [None]*len(source["x"])
    source["treeMode"][0] = "normal"

    return source, depth, int(width), level_width, acc

from Bokeh.ID3_Decision_Tree.id3_decision_tree import generate_tree, setActiveAttrs
import copy
import math


def get_depth(node, visited = {}):
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
    if node is None:
        return 0
    if level == 1:
        return 1
    elif level > 1:
        if node.parentPointer:
            node.depth = node.parentPointer.depth - 1
        return sum([get_width(child, level-1) for child in node.children])


def get_max_width(node, depth):
    max_width = 0
    h = depth
    level_widths = []
    for i in range(1, h+1):
        width = get_width(node, i)
        level_widths.append(width)
        if width > max_width:
            max_width = width
    return max_width, level_widths

# assign coords according to the max width of a level and node number
def generate_bokeh_data(source, root, depth, width, visited, level_width):
    width_index = [1] * depth

    queue = []
    queue.append(root)

    visited[root] = True

    while queue:

        popped_node = queue.pop(0)

        source["x"].append(2 * popped_node.depth)

        source["y"].append(width_index[popped_node.depth-1] + (width / (level_width[depth - popped_node.depth]+1)))

        if popped_node.children != []:
            source["nonLeafNodes_x"].append(2 * popped_node.depth)
            source["nonLeafNodes_y"].append(width_index[popped_node.depth - 1] + (width / (level_width[depth - popped_node.depth] + 1)))
            source["nonLeafNodes_stat"].append(popped_node.value)
            source["nonLeafNodes_decision"].append(popped_node.value)
            source["leafNodes_x"].append(None)
            source["leafNodes_y"].append(None)
        else:
            source["nonLeafNodes_x"].append(None)
            source["nonLeafNodes_y"].append(None)
            source["nonLeafNodes_stat"].append(None)
            source["nonLeafNodes_decision"].append(None)
            source["leafNodes_x"].append(2 * popped_node.depth)
            source["leafNodes_y"].append(width_index[popped_node.depth - 1] + (width / (level_width[depth - popped_node.depth] + 1)))


        if popped_node.name == "":
            source["attribute_type"].append("classAttr")
        else:
            source["attribute_type"].append(popped_node.name)

        source["stat_value"].append(popped_node.value)
        source["decision"].append(popped_node.decision)
        source["instanceCount"].append(len(popped_node.data))
        width_index[popped_node.depth - 1] += (width / (level_width[depth - popped_node.depth]+1))

        source["instances"].append(len(popped_node.data))

        for child in popped_node.children:
            if visited[child] == False:
                queue.append(child)
                visited[child] = True


def generate_node_list(root, visited):
    node_list = []

    queue = []
    queue.append(root)

    visited[root] = True

    while queue:

        popped_node = queue.pop(0)
        node_list.append(popped_node)

        for child in popped_node.children:
            if visited[child] == False:
                queue.append(child)
                visited[child] = True

    return node_list


def set_coord(node_list, level_width):

    for node in node_list[::-1]:
        if node.parentPointer:
            if node.width == 0:
                node.width = 1
            node.parentPointer.width += node.width


    level_width_index = 0
    passed_node = 0
    max_width = 0
    for level in range(len(level_width)):

        for i in range(passed_node, passed_node + level_width[level]):

            node_list[i].coord = ((2 * node_list[i].depth),
                                  (level_width_index + math.ceil(node_list[i].width / 2))
                                  )
            level_width_index += node_list[i].width


            # node_list[i].coord = (node_list[i].coord[0], node_list[i].coord[1]-1)
        if level_width_index > max_width:
            max_width = level_width_index

        passed_node += level_width[level]
        level_width_index = 0

    return max_width

def fill_source(source, node_list):
    for node in node_list:
        source["x"].append(node.coord[0])

        source["y"].append(node.coord[1])

        if node.name == "":
            source["attribute_type"].append("classAttr")
        else:
            source["attribute_type"].append(node.name)

        source["stat_value"].append(node.value)
        source["decision"].append(node.decision)
        source["instanceCount"].append(len(node.data))


def get_bokeh_data(method, activeAttrList = [], setRootAttribute=""):
    id_index = 0
    setActiveAttrs(activeAttrList)
    root, acc = generate_tree(method, setRootAttribute)

    visited = {}
    depth = get_depth(root, id_index, visited)
    width, level_width = get_max_width(root, depth)

    source = { "x": [], "y": [], "attribute_type": [], "instanceCount": [], "decision": [], "stat_value": []}

    node_list = generate_node_list(root, visited)
    max_width = set_coord(node_list, level_width)
    fill_source(source, node_list)

    # generate_bokeh_data(source, root, depth, width, visited, level_width)

    return source, depth, max_width, level_width, acc

get_bokeh_data("gini", [ "buyingAttr", "personsAttr", "lug_bootAttr", "safetyAttr", "classAttr" ])
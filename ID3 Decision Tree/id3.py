import pickle
import math
from copy import deepcopy

data  = pickle.load(open('car.pkl', 'rb'))
train = data['train']
test  = data['test']

# ##########################################################
# ########################Tree Node#########################


class Node:
    def __init__(self, attribute_type, instances, parent, children, instances_splitted, attribute_used, label_value):
        self.attribute_type = attribute_type
        self.instances = instances
        self.parent = parent
        self.children = children
        self.instances_splitted = instances_splitted
        self.attribute_used = attribute_used
        self.label_value = label_value


# ##########################################################

# ##########################################################
# ###############Attribute Informations#####################


attribute_value_array = [
    ["vhigh", "high", "med", "low"],
    ["vhigh", "high", "med", "low"],
    ["2", "3", "4", "5more"],
    ["2", "4", "more"],
    ["small", "med", "big"],
    ["low", "med", "high"],
    ["unacc", "acc", "good", "vgood"]
]

attribute_dict = {
    "buying": 0,
    "maint": 1,
    "doors": 2,
    "persons": 3,
    "lug_boot": 4,
    "safety": 5,
    "label"	: 6
}


# ##########################################################

# ##########################################################
# ###############Global Variables###########################

system_entropy = 0

# ##########################################################

# ##########################################################
# #################Entropy##################################
# Get instance numbers return entropy according to the label values


def entropy(instance_arr):
    entropy_arr = [0] * len(attribute_value_array[6])

    for i in instance_arr:
        entropy_arr[attribute_value_array[6].index(train[i][6])] += 1

    entropy_of_attribute = sum \
        ([((- x / sum(entropy_arr)) * math.log2(x /sum(entropy_arr))) for x in entropy_arr if x > 0])
    return entropy_of_attribute


# ##########################################################

# ##########################################################
# #################Information Gain#########################
                                                                                                                                          #
                                                                                                                                          #
def information_gain(instance_arr):                                                                                                       #
    entropy_of_attributes = [0] * 6                                                                                                       #
                                                                                                                                          #
    for i in range(0, 6):                                                                                                                 #
        for t in range(0, len(attribute_value_array[i])):                                                                                 #
            instances_of_attributes_value = [x for x in instance_arr if train[x][i] == attribute_value_array[i][t]]                       #
            entropy_of_attributes[i] += (len(instances_of_attributes_value) / len(instance_arr)) * entropy(instances_of_attributes_value) #

    information_gains = [system_entropy-x for x in entropy_of_attributes]
    return information_gains


# ##########################################################

# ##########################################################
# #################Gain Ratio#########################


def gain_ratio(instance_arr):
    info_gains = information_gain(instance_arr)
    split_info = [0] * 6

    split_array =   [
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0]
                    ]
    for instances in instance_arr:
        for att_arr_ind in range(0, len(attribute_value_array)-1):
            for val_ind in range(0, len(attribute_value_array[att_arr_ind])):
                if train[instances][att_arr_ind] == attribute_value_array[att_arr_ind][val_ind]:
                    split_array[att_arr_ind][val_ind] += 1

    for x in range(0, len(split_info)):
        a = sum([((-split_array[x][y]/sum(split_array[x])) * math.log2(split_array[x][y]/sum(split_array[x]))) for y in range(0, len(split_array[x]))])
        split_info[x] = a

    gain_ratios = [info_gains[x]/split_info[x] for x in range(0, len(info_gains))]
    return gain_ratios

###########################################################

###########################################################
##################Generate Tree Information Gain###########


def generate_node_info_gain(attribute_type, instances, parent, children, instances_splitted, attribute_used, label_value):
    new_node = Node(attribute_type, instances, parent, children, instances_splitted, attribute_used, label_value)

    information_gains = information_gain(instances)

    # Remove parents attribute types
    for x in range(0, len(attribute_used)):
        information_gains[attribute_used[x]] = -1

    # Set attribute type by getting max info gain
    for _type, value in attribute_dict.items():
        if value == information_gains.index(max(information_gains)):
            new_node.attribute_type = _type
            break

    # Split instances according to attribute type
    index_attribute_type = attribute_dict[new_node.attribute_type]
    for value in attribute_value_array[index_attribute_type]:
        new_node.instances_splitted.append( [x for x in instances if train[x][index_attribute_type] == value] )

    # Create children
    new_attribute_used = deepcopy(attribute_used)
    if attribute_dict[new_node.attribute_type] not in new_attribute_used:
        new_attribute_used.append(attribute_dict[new_node.attribute_type])
    for x in new_node.instances_splitted:
        if x != []:
            if entropy(x) == 0:
                new_node.children.append(Node("label", x, new_node, [], [], new_attribute_used, train[x[0]][6]))
            else:
                new_node.children.append(generate_node_info_gain(None, x, new_node, [], [], new_attribute_used, None))

    return new_node


###########################################################

##################Generate Tree Gain Ratio#################
###########################################################


def generate_node_gain_ratio(attribute_type, instances, parent, children, instances_splitted, attribute_used, label_value):
    new_node = Node(attribute_type, instances, parent, children, instances_splitted, attribute_used, label_value)

    gain_ratios = gain_ratio(instances)

    # Remove parents attribute types
    for x in range(0, len(attribute_used)):
        gain_ratios[attribute_used[x]] = -1

    # Set attribute type by getting max gain ratio
    for _type, value in attribute_dict.items():
        if value == gain_ratios.index(max(gain_ratios)):
            new_node.attribute_type = _type
            break

    # Split instances according to attribute type
    index_attribute_type = attribute_dict[new_node.attribute_type]
    for value in attribute_value_array[index_attribute_type]:
        new_node.instances_splitted.append([x for x in instances if train[x][index_attribute_type] == value])

    # Create children
    new_attribute_used = deepcopy(attribute_used)
    if attribute_dict[new_node.attribute_type] not in new_attribute_used:
        new_attribute_used.append(attribute_dict[new_node.attribute_type])
    for x in new_node.instances_splitted:
        if x != []:
            if entropy(x) == 0:
                new_node.children.append(Node("label", x, new_node, [], [], new_attribute_used, train[x[0]][6]))
            else:
                new_node.children.append(generate_node_info_gain(None, x, new_node, [], [], new_attribute_used, None))

    return new_node


###########################################################

##################Generate Tree Gini Index#################
###########################################################


def generate_node_gini_index(attribute_type, instances, parent, children, instances_splitted, attribute_used, label_value):
    new_node = Node(attribute_type, instances, parent, children, instances_splitted, attribute_used, label_value)



###########################################################

###########################################################
##################Draw Tree############################


def draw_tree(f, node, indent):
    indent += "____"
    if node.attribute_type != "label":
        f.write(indent + "Attr :" + node.attribute_type + " #instances :" + str(len(node.instances)) + "\n")
        for child in node.children:
            draw_tree(f, child, indent)
    else:
        f.write(indent + "Value :" + node.label_value + " #instances :" + str(len(node.instances)) + "\n")


###########################################################

###########################################################
##################Generate Tree############################


def generate_tree():
    global system_entropy
    instance_indexes = [i for i in range(0, len(train))]
    system_entropy = entropy(instance_indexes)

    root_info_gain  = generate_node_info_gain(None, instance_indexes, None, [], [], [], None)
    root_gain_ratio = generate_node_gain_ratio(None, instance_indexes, None, [], [], [], None)

    f = open("tree_info_gain.txt", "w")
    draw_tree(f, root_info_gain, "")
    f.close()
    f = open("tree_gain_ratio.txt", "w")
    draw_tree(f, root_gain_ratio, "")
    f.close()

    return root_info_gain, root_gain_ratio

###########################################################

###########################################################
##################Generate Tree############################


def test_tree(root):
    node = root
    true = 0
    false = 0
    for instance in test:
        while node.attribute_type != "label":
            node = node.children[attribute_value_array[attribute_dict[node.attribute_type]].index(instance[attribute_dict[node.attribute_type]])]
        if node.label_value == instance[6]:
            true += 1
        else:
            false += 1
    print("Correct Classified :", true, " False Classified :", false)
    print("Acc :", true/(true+false))

###########################################################


def main():
    root_info_gain, root_gain_ratio = generate_tree()
    test_tree(root_info_gain)
    test_tree(root_gain_ratio)


if __name__ == '__main__':
    main()

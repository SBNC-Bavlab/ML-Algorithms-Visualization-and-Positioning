import copy
from queue import Queue
import random
from Bokeh.Plot.getChoice import get_choice
from Bokeh.Plot.dictionaries import modify_new_values, get_new_values, get_class_attr, get_test_set, \
    get_train_set, set_active_attr
from math import log
attrNamesList = []
attrDictionary = {}
classAttr = []

class Node(object):
    """ Tree node """
    def __init__(self, parent_name, name, data, children, rem_attr, method):
        self.parent = parent_name
        self.parentPointer = Node
        self.name = name
        self.data = data
        self.children = children
        self.remainingAttributes = rem_attr
        self.decision = None
        self.method = method
        self.value = None
        self.width = 0
        self.coord = (0, 0)

        self.prelim = 0
        self.mod = 0
        self.thread = None
        self.ancestor = self
        self.order_number = 1
        self.change = 0
        self.shift = 0

def entropy(distribution_list_var):
    """ Calculate uncertainty of the nodes instances"""
    number_of_instances = 0.0
    for dist in distribution_list_var:
        number_of_instances += dist

    if number_of_instances == 0:
        return 0

    entropy_sum = 0.0
    for dist in distribution_list_var:
        percentage = float(dist) / float(number_of_instances)
        if percentage == 0:
            entropy_holder = 0.0
        else:
            log_value = log(percentage, 4)
            entropy_holder = percentage * log_value * -1
        entropy_sum += entropy_holder

    return float(entropy_sum)


def classify_list(attribute_name_var, instances_var):
    """ Return a list that divide the instances according to the values of a attribute"""
    """ For instance, there is a attribute which has values like "low", "med", "high" """
    """ There are 100 instances. For every instances, the attributes values distribute like [30, 40, 30]"""
    attribute = attrDictionary[attribute_name_var]
    attribute_index, attribute_values = attribute
    local_distribution = []

    for attributeValue in attribute_values:
        counter = 0
        for instance in instances_var:
            if instance[attribute_index] == attributeValue:
                counter += 1
        local_distribution.append(counter)

    return local_distribution


def get_distribution_list(attribute_name_var, instances_var):
    """ Return nested list that divide the instances according to the values of the label"""
    """ For instance, there is a attribute which has values like "low", "med", "high" """
    """ There are 100 instances. For every instances, the number of instances distribute like [30, 40, 30]"""
    """ For instance, label values are like "un_acc", "acc", "good", "v_good" """
    """ Instances divide according to the label values like [[10, 5, 15, 0], [10, 10, 10, 10], [4, 13, 3, 10]]"""
    # build a distribution holder
    attribute = attrDictionary[attribute_name_var]
    attribute_index, attribute_values = attribute
    distribution = []

    # find distribution of class based of values of an attribute

    for attributeValue in attribute_values:
        local_distribution = [0] * len(classAttr)

        for instance in instances_var:
            if instance[attribute_index] == attributeValue:
                class_value = instance[-1]
                class_index = classAttr.index(class_value)
                local_distribution[class_index] += 1
        distribution.append(local_distribution)

    return distribution


def feature_length(attribute_name_var):
    """ Return number of a attribute values """
    attribute = attrDictionary[attribute_name_var]
    attribute_index, attribute_values = attribute
    return len(attribute_values)


def information(attribute_name_var, instances_var):
    """ Calculate the information of a node """
    """ Calculate the information of every branch of a node and sum them"""
    distribution_list = get_distribution_list(attribute_name_var, instances_var)
    number_of_instances = len(instances_var)

    information_sum = 0.0
    for localDistribution in distribution_list:
        number_of_instances_in_local = sum(localDistribution)
        proportion_to_all = float(number_of_instances_in_local) / number_of_instances
        local_entropy = entropy(localDistribution)

        element = proportion_to_all * local_entropy
        information_sum += element

    return information_sum


def information_gain(attribute_name_var, instances_var):
    """ Calculate the information gain by subtracting node information from system entropy"""
    global_distribution_list = classify_list("classAttr", instances_var)
    entropy_value = entropy(global_distribution_list)

    information_value = information(attribute_name_var, instances_var)
    information_gain_value = entropy_value - information_value
    return information_gain_value


def log_for_intrinsic_information(proportion_to_all, number_of_different_values):
    """ Checking proportion to avoid division error"""
    if proportion_to_all == 0:
        return 0
    else:
        return log(proportion_to_all, number_of_different_values)


def intrinsic_information(attribute_name_var, instances_var):
    """ Calculate every branch proportion and sum of them to find node's intrinsic information"""
    distribution_list = get_distribution_list(attribute_name_var, instances_var)
    number_of_different_values = feature_length(attribute_name_var)
    number_of_instances = len(instances_var)

    intrinsic_sum = 0.0
    for localDistribution in distribution_list:
        n_of_instances_in_local = sum(localDistribution)
        proportion_to_all = float(n_of_instances_in_local) / number_of_instances
        log_of_proportion = log_for_intrinsic_information(proportion_to_all, number_of_different_values)

        element = -1 * proportion_to_all * log_of_proportion
        intrinsic_sum += element
    return intrinsic_sum


def gain_ratio(attribute_name_var, instances_var):
    """ Calculate gain ratio by dividing gain to intrinsic information"""
    gain_value = information_gain(attribute_name_var, instances_var)
    intrinsic_information_value = intrinsic_information(attribute_name_var, instances_var)

    gain_ratio_value = gain_value / intrinsic_information_value
    return gain_ratio_value


def gini(distribution_list_var):
    """ Calculate gini value of the node by subtracking sum of proportion of branches from 1"""
    number_of_instances = sum(distribution_list_var)
    if number_of_instances == 0:
        return 0

    sum_of_squares = 0.0
    for number in distribution_list_var:
        proportion_to_all = float(number)/number_of_instances
        sum_of_squares += proportion_to_all**2
    gini_value = 1 - sum_of_squares
    return gini_value


def gini_index(attribute_name_var, instances_var):
    """ gini Index of that attribute"""
    distribution_list = get_distribution_list(attribute_name_var, instances_var)
    number_of_instances = len(instances_var)

    gini_index_value = 0.0
    for localDistribution in distribution_list:
        number_of_instances_in_local = sum(localDistribution)
        if number_of_instances == 0:
            proportion_to_all = 0
        else:
            proportion_to_all = float(number_of_instances_in_local) / number_of_instances
        gini_value = gini(localDistribution)

        element = proportion_to_all * gini_value
        gini_index_value += element

    return gini_index_value


def choose_the_best(attribute_list_var, instances_var, methodology):
    """ Best attribute to divide remaining instances according to the methods value"""
    values_list = []
    for attr in attribute_list_var:
        if methodology == "gini":
            value = gini_index(attr, instances_var)
        elif methodology == "gainRatio":
            value = gain_ratio(attr, instances_var)
        else:
            value = information_gain(attr, instances_var)
        values_list.append(value)

    if methodology == "gini":
        index = values_list.index(min(values_list))
        value = min(values_list)
    else:
        index = values_list.index(max(values_list))
        value = max(values_list)

    return attribute_list_var[index], value


def distribute_by_attribute(attribute_name_var, instances_var):
    """ Divide instances by values of a attribute """
    attribute = attrDictionary[attribute_name_var]
    attribute_index, attribute_values = attribute
    distribution = []

    # find distribution of class based of values of an attribute
    for attributeValue in attribute_values:
        local_distribution = []

        for instance in instances_var:
            if instance[attribute_index] == attributeValue:
                local_distribution.append(instance)
        distribution.append(local_distribution)

    return distribution


def child_generator(node_itself_var, methodology):
    """
        Generate children and set them to their parent
    """
    parent_name = node_itself_var.name
    instances = node_itself_var.data
    remaining_attributes = node_itself_var.remainingAttributes
    distributed_list = distribute_by_attribute(parent_name, instances)

    parent_leaf_check = leaf_control(node_itself_var)
    if parent_leaf_check:
        return []

    # leaf node
    if remaining_attributes == [] and instances != []:
        determine_dominant_one(node_itself_var)
        node_itself_var.children = []
        return []

    # never happens, yet for safety concerns
    if instances is []:
        # print("NO instances left")
        node_itself_var.children = []
        return []

    # generate children
    children = []
    for dataPart in distributed_list:
        child_node = Node(parent_name, "", dataPart, [], [], methodology)
        child_node.parentPointer = node_itself_var
        is_leaf = leaf_control(child_node)

        if dataPart is []:
            child_node = Node(parent_name, "", dataPart, [], [], methodology)
            child_node.parentPointer = node_itself_var

        elif is_leaf:
            child_node = Node(parent_name, "", dataPart, [], [], methodology)
            child_node.parentPointer = node_itself_var
            determine_dominant_one(child_node)

        else:
            children_attr_name, success_value = choose_the_best(remaining_attributes, dataPart, methodology)
            child_remaining_attr_list = copy.deepcopy(remaining_attributes)
            child_remaining_attr_list.remove(children_attr_name)

            child_node = Node(parent_name, children_attr_name, dataPart, [], child_remaining_attr_list, methodology)
            child_node.parentPointer = node_itself_var
            child_node.value = success_value

        children.append(child_node)

    # set children
    node_itself_var.children = children
    return children


def leaf_control(node_var):
    """
        Check if the node's instances distributed to certain value
    """
    distributed_list = classify_list("classAttr", node_var.data)
    numbers_greater_than_zero = 0
    for p in distributed_list:
        if p > 0:
            numbers_greater_than_zero += 1

    if numbers_greater_than_zero == 1:
        return True
    else:
        return False


def determine_dominant_one(node_var):
    """
        If there is no remaining attribute to divide instances than
        determine the decision by looking remaining instances label values
    """
    instances = node_var.data
    distributed_list_on_class_attr = classify_list("classAttr", instances)

    max_occurrence = max(distributed_list_on_class_attr)
    max_indexes = []
    for i in range(len(distributed_list_on_class_attr)):
        if distributed_list_on_class_attr[i] == max_occurrence:
            max_indexes.append(i)

    chosen_index = random.choice(max_indexes)
    dominant_class_index = chosen_index
    dominant_class_name = classAttr[dominant_class_index]
    node_var.decision = dominant_class_name


def observe_from_siblings(node_var):
    """
        If there is no instance to classify a leaf then choose its decision by checking siblings decisions
    """
    siblings = node_var.parentPointer.children

    siblings_distributions = [0] * len(classAttr)
    for sibling in siblings:
        sibling_dist = classify_list("classAttr", sibling.data)
        for i in range(len(sibling_dist)):
            siblings_distributions[i] += sibling_dist[i]

    max_index = siblings_distributions.index(max(siblings_distributions))
    max_name = classAttr[max_index]
    node_var.decision = max_name


def tree_distribution(attribute_list_var, instances_var, methodology, set_root_attribute):
    """
        Set root, start to divide data set and assign children
    """
    attrib_list_copy = copy.deepcopy(attribute_list_var)
    instances_copy = copy.deepcopy(instances_var)

    if set_root_attribute == "":
        # this is the root node
        best_attr_name, success_value = choose_the_best(attrib_list_copy, instances_copy, methodology)
        attrib_list_copy.remove(best_attr_name)
        root_node = Node("", best_attr_name, instances_copy, [], attrib_list_copy, methodology)
        root_node.parentPointer = None
        root_node.value = success_value

    else:
        if methodology == "gini":
            value = gini_index(set_root_attribute, instances_var)
        elif methodology == "gainRatio":
            value = gain_ratio(set_root_attribute, instances_var)
        else:
            value = information_gain(set_root_attribute, instances_var)

        attrib_list_copy.remove(set_root_attribute)
        root_node = Node("", set_root_attribute, instances_copy, [], attrib_list_copy, methodology)
        root_node.parentPointer = None
        root_node.value = value

    q = Queue()
    q.put(root_node)
    while not q.empty():
        node = q.get()
        if len(node.data) == 0:
            continue
        child_list = child_generator(node, methodology)
        for child in child_list:
            if leaf_control(child):
                continue
            else:
                q.put(child)

    review_queue = Queue()
    review_queue.put(root_node)
    while not review_queue.empty():

        node = review_queue.get()
        for child in node.children:
            review_queue.put(child)

        # optimize for "noInfo" nodes
        if len(node.data) == 0:
            observe_from_siblings(node)

    return root_node


def make_guess(root_node_var, test_instance_var):
    """
        Get test instance decision from tree
    """
    flag = True
    node = root_node_var
    decision = ""
    while flag:
        if node.decision is not None:
            decision = node.decision
            break
        if node.decision is None and node.name == "":
            decision = "?"
            break
        attribute = attrDictionary[node.name]
        attribute_index, attribute_values = attribute

        feature_value = test_instance_var[attribute_index]
        feature_index = attribute_values.index(feature_value)

        node = node.children[feature_index]
    return decision


def real_world_test(root_node_var, instances_var):
    """
        Test instances and return the percentage
    """
    valid = 0
    invalid = 0
    for ins in instances_var:
        guess = make_guess(root_node_var, ins)
        if guess == ins[-1]:
            valid += 1
        else:
            invalid += 1
    return valid/float(valid+invalid)


def dataset_same(tmp_attr_names, attr_names_list):
    """
        Check data set is new
    """
    for i in tmp_attr_names:
        if i in attr_names_list and i != "classAttr":
            return True
    return False


def generate_tree(method, set_root_attribute, activeAttrList):
    """
        Generate tree
    """
    global test, train, attrNamesList, attrDictionary, classAttr
    attrNamesList = set_active_attr(activeAttrList)
    tmp_attr_names = attrNamesList
    attrNamesList, attrDictionary = get_new_values()
    if dataset_same(tmp_attr_names, attrNamesList):
        attrNamesList, attrDictionary = modify_new_values(tmp_attr_names, attrNamesList, attrDictionary)
    new_att_name_list = copy.deepcopy(attrNamesList)
    new_att_name_list.remove("classAttr")
    test = get_test_set()
    train = get_train_set()
    classAttr = get_class_attr()
    root_node = tree_distribution(new_att_name_list, train, method, set_root_attribute)

    return root_node, real_world_test(root_node, test)

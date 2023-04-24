from main import Node, Tree
import json

def from_dict(file_name):
    with open(f"{file_name}", "r") as file:
        data = json.load(file)
        Root_node = Node('Movie')
        for key in list(data.keys()):
            main_node = Node(f'{key}')
            for children in data[key]:
                child_node = Node(children)
                main_node.add_child(child_node)
                if type(data[key]) == dict:
                    for child_child in data[key][children] :
                        child_node.add_child(Node(child_child))

            Root_node.add_child(main_node)
        tree_ret = Tree()
        tree_ret.add_root(Root_node)
        tree_ret.traverse_tree(tree_ret.root)

if __name__ == '__main__':
    from_dict('data.json')
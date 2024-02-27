from typing import Union

from json import load, dump
from queue import Queue

from yaml import safe_load

from ego.entity.dto.tree.Node import Node

from ego.utils.collections.ListUtil import insert


class ConfigHandler:
    def __init__(
            self,
            yml_path=None, json_path=None,
            yml_stream=None, json_stream=None,
            src_json=None,
            encoding="utf-8"
    ):
        if yml_path:
            with open(yml_path, mode="r", encoding=encoding) as file:
                self.__src_json = safe_load(file)
        if json_path:
            with open(json_path, mode="r", encoding=encoding) as file:
                self.__src_json = load(file)
        if yml_stream:
            self.__src_json = safe_load(yml_stream)
        if json_stream:
            self.__src_json = load(json_stream)
        if src_json:
            self.__src_json = src_json

        self.__dist = {}
        self.__node_queue = Queue()
        self.__list_cache_queue = Queue()
        self.__child: Union[Node, None] = None

    def set_source_json(self, src):
        self.__src_json = src

    def get_source_json(self):
        return self.__src_json

    def get_dist(self):
        return self.__dist

    def __handle_dict(self):
        node = self.__child.get_node()
        parent_id = self.__child.get_parent_id()
        for key in node:
            next_parent_id = f"{parent_id}.{key}"
            value = node[key]

            v_type = type(value)
            if v_type == dict or v_type == list:
                self.__node_queue.put(Node(parent_id=next_parent_id, node=value))
                continue

            self.__dist[next_parent_id] = value

    def __handle_list(self):
        node = self.__child.get_node()
        parent_id = self.__child.get_parent_id()
        index = 0
        for value in node:
            next_parent_id = f"{parent_id}[{index}]"
            index += 1

            v_type = type(value)
            if v_type == dict or v_type == list:
                self.__node_queue.put(Node(parent_id=next_parent_id, node=value))
                continue

            self.__dist[next_parent_id] = value

    def __iterate_child(self):
        node = self.__child.get_node()
        c_type = type(node)
        if c_type == dict:
            self.__handle_dict()
            return

        if c_type == list:
            self.__handle_list()
            return

        key, = node
        value, = node.values()
        self.__dist[f"{self.__child.get_parent_id()}.{key}"] = value

    def iteration(self):
        if type(self.__src_json) == dict:
            for key in self.__src_json:
                value = self.__src_json[key]
                v_type = type(value)

                if v_type == dict or v_type == list:
                    self.__node_queue.put(Node(parent_id=key, node=value))
                    continue

                self.__dist[key] = value
        else:
            index = 0
            for value in self.__src_json:
                this_id = f"[{index}]"
                index += 1

                s_type = type(value)
                if s_type == dict or s_type == list:
                    self.__node_queue.put(Node(parent_id=this_id, node=value))
                    continue

                self.__dist[this_id] = value
                print(f"{this_id}={value}")

        while not self.__node_queue.empty():
            self.__child = self.__node_queue.get()
            self.__iterate_child()

    def __handle_reverse_p_dict(self):
        node = self.__child.get_node()
        key, = node
        value, = node.values()

        c_keys = key.split('.', 1)
        p_key = c_keys[0]

        if p_key.find('[') == 0:
            if len(c_keys) == 1:
                if not self.__child.get_parent()[self.__child.get_parent_id()]:
                    self.__child.get_parent()[self.__child.get_parent_id()] = []
                insert(
                    self.__child.get_parent()[self.__child.get_parent_id()],
                    int(key.replace('[', '').replace(']', '')),
                    value
                )
                return

            if '][' in p_key:
                this_ids = p_key.split('][', 1)
                index = int(this_ids[0].replace('[', ""))
                node_key = f"[{this_ids[1]}"
                if len(c_keys) > 1:
                    node_key = f"{node_key}.{c_keys[1]}"
            else:
                index = int(p_key.replace('[', "").replace(']', ""))
                node_key = c_keys[1]

            child = {node_key: value}
            self.__handle_reverse_list(index, child, False)
            return

        if len(c_keys) > 1:
            if '[' in p_key:
                this_ids = p_key.split('[')
                p_key = this_ids[0]
                node_key = f"[{this_ids[1]}.{c_keys[1]}"
            else:
                node_key = c_keys[1]

            child = {node_key: value}
            self.__handle_reverse_dict(p_key, child)
            return

        if '[' in p_key:
            this_ids = p_key.split('[')
            p_key = this_ids[0]
            node_key = f"[{this_ids[1]}"

            child = {node_key: value}
            self.__handle_reverse_dict(p_key, child)
            return

        self.__set_reverse_value()

    def __handle_reverse_p_list(self):
        self.__list_cache_queue.put(Node(parent=self.__dist, node=None))

        node = self.__child.get_node()
        key, = node
        value, = node.values()

        c_keys = key.split('.', 1)
        p_key = c_keys[0]

        if p_key.find('[') == 0:
            if len(c_keys) == 1:
                if not self.__child.get_parent()[self.__child.get_parent_id()]:
                    self.__child.get_parent()[self.__child.get_parent_id()] = []
                insert(
                    self.__child.get_parent()[self.__child.get_parent_id()],
                    int(key.replace('[', '').replace(']', '')),
                    value
                )
                return

            if '][' in p_key:
                this_ids = p_key.split('][', 1)
                index = int(this_ids[0].replace('[', ""))
                node_key = f"[{this_ids[1]}"
                if len(c_keys) > 1:
                    node_key = f"{node_key}.{c_keys[1]}"
            else:
                index = int(p_key.replace('[', "").replace(']', ""))
                node_key = c_keys[1]

            child = {node_key: value}
            self.__handle_reverse_list(index, child)
            return

        if len(c_keys) > 1:
            if '[' in p_key:
                this_ids = p_key.split('[')
                p_key = this_ids[0]
                node_key = f"[{this_ids[1]}.{c_keys[1]}"
            else:
                node_key = c_keys[1]

            child = {node_key: value}
            self.__handle_reverse_dict(p_key, child)
            return

        if '[' in p_key:
            this_ids = p_key.split('[')
            p_key = this_ids[0]
            node_key = f"[{this_ids[1]}"

            child = {node_key: value}
            self.__handle_reverse_dict(p_key, child)
            return

        self.__set_reverse_value()

    def __handle_reverse_dict(self, p_key, child):
        parent_id = self.__child.get_parent_id()
        parent = self.__child.get_parent()

        if parent[parent_id] is None:
            parent[parent_id] = {}

        if p_key not in parent[parent_id]:
            parent[parent_id][p_key] = None
        self.__node_queue.put(Node(parent_id=p_key, parent=parent[parent_id], node=child))

    def __handle_reverse_list(self, index, child, up_is_list=True):
        parent_id = self.__child.get_parent_id()
        parent = self.__child.get_parent()

        if not up_is_list:
            if parent[parent_id] is None:
                parent[parent_id] = []
            self.__node_queue.put(Node(parent_id=index, parent=parent[parent_id], node=child, parent_is_dict=False))
            return

        insert(parent, index, -1)

    def __set_reverse_value(self):
        parent_id = self.__child.get_parent_id()
        parent = self.__child.get_parent()
        node = self.__child.get_node()

        p_type = type(parent)
        n_type = type(node)

        if p_type == list:
            if n_type == list:
                parent.extends(node)
                return

            if n_type == dict and len(parent) > parent_id:
                parent[parent_id].update(node)
                return

            insert(parent, parent_id, node)
            return

        if p_type == dict:
            if n_type == dict:
                if parent[parent_id] is None:
                    parent[parent_id] = {}

                parent[parent_id].update(node)
                return

            if n_type == list:
                if parent[parent_id] is None:
                    parent[parent_id] = []

                parent[parent_id].extends(node)
                return

    def __iterate_reverse_child(self):
        parent_is_dict = self.__child.parent_is_dict

        if parent_is_dict:
            self.__handle_reverse_p_dict()
            return

        if not parent_is_dict:
            self.__handle_reverse_p_list()

    def iteration_reverse(self):
        for key in self.__src_json:
            value = self.__src_json[key]

            keys = key.split('.', 1)
            this_id = keys[0]

            if this_id.find('[') == 0:
                if '][' in this_id:
                    this_ids = this_id.split('][', 1)
                    index = int(this_ids[0].replace('[', ""))
                    node_key = f"[{this_ids[1]}"
                    if len(keys) > 1:
                        node_key = f"{node_key}.{keys[1]}"
                else:
                    index = int(this_id.replace('[', "").replace(']', ""))
                    node_key = keys[1]

                if self.__dist == {}:
                    self.__dist = []

                node = {node_key: value}
                self.__node_queue.put(Node(parent_id=index, parent=self.__dist, node=node, parent_is_dict=False))
                continue

            if len(keys) > 1:
                if '[' in this_id:
                    this_ids = this_id.split('[', 1)
                    this_id = this_ids[0]
                    node_key = f"[{this_ids[1]}.{keys[1]}"
                else:
                    node_key = keys[1]

                if this_id not in self.__dist:
                    self.__dist[this_id] = None
                node = {node_key: value}
                self.__node_queue.put(Node(parent_id=this_id, parent=self.__dist, node=node))
                continue

            if '[' in this_id:
                this_ids = this_id.split('[', 1)
                this_id = this_ids[0]
                node_key = f"[{this_ids[1]}"

                if this_id not in self.__dist:
                    self.__dist[this_id] = []
                node = {node_key: value}
                self.__node_queue.put(Node(parent_id=this_id, parent=self.__dist, node=node))
                continue

            self.__dist[key] = value

        while not self.__node_queue.empty():
            self.__child = self.__node_queue.get()
            self.__iterate_reverse_child()


if __name__ == "__main__":
    print("Conversion start...")
    # 转换
    ypath = ""
    handler = ConfigHandler(yml_path=ypath)
    # jpath = ""
    # handler = ConfigHandler(json_path=jpath)
    handler.iteration()
    print(handler.get_source_json())
    print(handler.get_dist())
    json_file_path = ""
    with open(file=json_file_path, mode="w+", encoding="utf-8") as file_obj:
        dump(handler.get_dist(), file_obj)

    # 逆转
    # r_json_path = ""
    handler = ConfigHandler(json_path=json_file_path)
    handler.iteration_reverse()
    print(handler.get_dist())

# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

class Mapping(object):
    """
    hash可能オブジェクトに整数のナンバリングを行う。
    これらのマッピングを管理する。
    """
    def __init__(self, naming=None, start_num=0):
        # obj -> node
        self.mapping = {}
        # node -> obj
        self.rev_map = {}

        self.count = start_num-1
        if naming is None:
            self.naming = self.naming_default
        else:
            self.naming = naming

    def increment(self):
        self.count += 1
        return self.count

    def register(self, obj):
        if obj not in self.mapping:
            self.mapping[obj] = self.naming(self.increment())
            self.rev_map[self.mapping[obj]] = obj
        return self.mapping[obj]

    def naming_default(self, obj):
        return obj

    def __contains__(self, obj):
        return obj in self.mapping

    def __len__(self):
        return len(self.mapping)

    def __call__(self, obj):
        """
        obj -> node
        """
        if obj not in self.mapping:
            self.register(obj)
        return self.mapping[obj]

    def rev(self, node):
        """
        node -> obj
        """
        return self.rev_map[node]

    def __str__(self):
        return "\n".join([f"{k}:{v}" for k, v in self.mapping.items()])

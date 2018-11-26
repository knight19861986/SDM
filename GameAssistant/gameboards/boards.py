# -*- coding: utf-8 -*-
import random

class Role(object):
    def __init__(self, name, description, maximum=1):
        self.name = name
        self.description = description
        self.maximum = maximum

    def __str__(self):
        return self.name


class Board(object):
    # name = 'BoardGame'
    # roles = []
    def __init__(self, role_dict={}):
        self.role_dict = role_dict
        self.role_index = {}
        for role in self.roles:
            self.role_index[role.name] = role

    def get_description(self, role_name):
        return self.role_index[role_name].description

    def get_maximum(self, role_name):
        return self.role_index[role_name].maximum

    def deal(self):
        res = []
        for key, value in self.role_dict.items():
            if key in self.role_index:
                role_name = key
            else: 
                role_name = 'Unknown'
            for i in range(value):
                res.append(role_name)
        random.seed()
        random.shuffle(res)
        return res

    def __str__(self):
        return self.name


# -*- coding: utf-8 -*-
import random

class Role(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name


class Board(object):
    # name = 'BoardGame'
    # roles = []
    def __init__(self, role_dict={}):
        self.role_dict = role_dict

    def deal(self):
        res = []        
        for key, value in self.role_dict.items():
            if key in [role.name for role in self.roles]:
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


# -*- coding: utf-8 -*-
# © 2017 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def dict_compare(d1, d2):
    assert len(d1) == len(d2)
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    assert len(intersect_keys) == len(d1)
    for key in d1_keys:
        assert d1[key] == d2[key]


def rdns_to_map(data):
    count=0
    token=""
    pos_comma=0
    pos_equal=0
    value={}
    llave=""
    for x in data:
        if x==',':
            pos_comma = count
        if x=='=':
            if llave!="":
                value[llave] = data[pos_equal+1:pos_comma]
            pos_equal=count
            llave=data[pos_comma:pos_equal]
        count+=1
    value[llave] = data[pos_equal+1:len(data)]
    return value
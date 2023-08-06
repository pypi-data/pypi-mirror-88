#!/usr/bin/env python
# -*- coding:utf-8 -*-
from restsql.exception import JsonFormatException, ProgramConfigException


def _parse_fields_or_export(fields):
    """
    将real@alias的字符串列表转为real2alias的映射map
    :param fields: real@alias的字符串列表
    :return: real2alias的映射map
    """
    real_alias_map = {}
    for field in fields:
        real, alias = field.split('@', 1)
        real_alias_map[real] = alias
    return real_alias_map


class Aggregation:
    AVG = 'avg'
    SUM = 'sum'
    MAX = 'max'
    MIN = 'min'
    COUNT = 'count'
    COUNT_DISTINCT = 'count_distinct'

    def __init__(self, agg_str):
        """
        将aggregation字段的字符串拆分为field和后缀部分
        :param agg_str: aggregation字段字符串
        """
        self.field, self.suffix = agg_str.rsplit('__', 1)


class Filter:
    EQUAL = 'eq'  # TODO：修改前端，添加eq后缀
    GT = 'gt'
    GTE = 'gte'
    LT = 'lt'
    LTE = 'lte'
    CONTAINS = 'contains'
    STARTS_WITH = 'startswith'
    ENDS_WITH = 'endswith'
    RANGE = 'range'
    IN = 'in'

    def __init__(self, key, value):
        self.value = value
        if key.find('__') == -1:  # 前端逻辑问题：无后缀为eq，不方便后端判断。
            self.key = key
            self.suffix = Filter.EQUAL
        else:
            self.key, self.suffix = key.rsplit('__', 1)


class Select:
    """
    select数据类。存储着query.select内的数据。
    """

    def __init__(self, select_dict):
        self.from_ = select_dict.get('from', '')  # 后下划线为了区别python关键字from
        self.fields = select_dict.get('fields', [])
        self.filter = Select._parse_filter(select_dict.get('filter', {}))
        self.aggregation = Select._parse_aggregation(select_dict.get('aggregation', []))
        self.group_by = select_dict.get('group_by', [])
        self.limit = select_dict.get('limit', 1000)

    @staticmethod
    def _parse_aggregation(agg_list):
        return [Aggregation(agg_str) for agg_str in agg_list]

    @staticmethod
    def _parse_filter(filter_dict):
        return [Filter(key, value) for key, value in filter_dict.items()]


def _parse_join(joins):
    """
    转换join为QueryObject的list
    :param joins: 类型不是QueryType.MAIN的同源query的list
    :return: QueryObject的list
    """
    return [QueryObject(join) for join in joins]


class QueryObject:
    MAIN = 'main'
    LEFT_JOIN = 'left_join'  # LEFT OUTER JOIN
    INNER_JOIN = 'inner_join'  # INNER JOIN
    FULL_JOIN = 'full_join'  # FULL JOIN
    """
    query数据类。存储整个query的数据。

    """

    def __init__(self, json_dict):
        """
        生成QueryObject对象，用于后续查询。
        注意，请保证attach到main query的sub query与main query同源。
        :param json_dict: query或join的json内容
        """
        if isinstance(json_dict, dict):
            self.type = json_dict.get('type', QueryObject.MAIN)
            if self.type == QueryObject.MAIN:  # 为什么要这么分两类? 为了将同源的查询合入
                self.sort = json_dict.get('sort', [])
                self.fields = _parse_fields_or_export(json_dict.get('fields', []))
                self.limit = json_dict.get('limit', 1000)
                if 'select' not in json_dict:
                    raise JsonFormatException(1, 'Json格式错误: 无select部分。')
                self.select = Select(json_dict['select'])
                self.join = _parse_join(json_dict.get('join', []))
            else:
                self.on = json_dict.get('on', {})
                self.export = _parse_fields_or_export(json_dict.get('export', []))
                self.select = Select(json_dict['query']['select'])
        else:
            raise ProgramConfigException(1, '参数错误。需要指定格式化的json字典，而不是%s。', type(json_dict))

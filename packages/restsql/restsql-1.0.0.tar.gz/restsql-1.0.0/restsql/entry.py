#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import sys

from restsql.engine import Engine
from restsql.exception import ProgramConfigException, RunningException
from restsql.model import QueryObject


class RestSQL:
    """
    RestSQL服务提供类。对外提供json查询数据库的服务。
    """

    def __init__(self):
        pass

    @staticmethod
    def query(json_dict_list, engine, conn):
        """
        对外查询入口。
        传入已经按照源拆分的json字典，并将主查询放第一位，将会join、sort后返回dataframe。
        注意事项：
        1. 请将**主查询放到第一位**。
        2. 若是elasticsearch查询，请直接拆分为list。es暂不支持同源查询。
        > 为什么要设计成传入不同源list而不是直接传入原json dict后在内部拆分呢？因为同源的判断需要用到table_map，这部分不应该出现在restsql lib中。
        :return: dataframe存储的结果
        """
        query_object_list = [QueryObject(json_dict) for json_dict in json_dict_list]
        result_df_list = [RestSQL._query_by_same_source(query_object, engine, conn) for query_object in
                          query_object_list]
        main_result_df = result_df_list.pop(0)
        # Join
        for idx, result_df in enumerate(result_df_list):
            query_object = query_object_list[idx + 1]
            if query_object.type == QueryObject.LEFT_JOIN:  # 不知道为什么，keys外必须包裹一层keys
                main_result_df = main_result_df.merge(result_df, left_on=list(query_object.on.keys()),
                                                      right_on=list(query_object.on.values()), how='left')
            elif query_object.type == QueryObject.INNER_JOIN:
                main_result_df = main_result_df.merge(result_df, left_on=list(query_object.on.keys()),
                                                      right_on=list(query_object.on.values()), how='inner')
            elif query_object.type == QueryObject.FULL_JOIN:
                main_result_df = main_result_df.merge(result_df, left_on=list(query_object.on.keys()),
                                                      right_on=list(query_object.on.values()), how='outer')
            else:
                raise ProgramConfigException(1, '请联系开发者: main查询必须在列表第一位。')
        # Sort
        if len(query_object_list[0].sort) != 0:
            ascending_sort = []
            for idx, val in enumerate(query_object_list[0].sort):  # 将'-'号设为倒序，无前缀设为正序
                if val.startswith('-'):
                    query_object_list[0].sort[idx] = val[1:]
                    ascending_sort.append(False)
                else:
                    ascending_sort.append(True)
            main_result_df.sort_values(by=query_object_list[0].sort, ascending=ascending_sort, inplace=True)
        # Limit
        main_result_df.drop(labels=range(query_object_list[0].limit, main_result_df.shape[0]), axis=0, inplace=True)
        # Alias and expression
        exclude_list = []
        columns_list = main_result_df.columns.tolist()
        for column in columns_list:
            if column in query_object_list[0].fields.keys():  # 重命名
                if query_object_list[0].fields[column] != column:
                    main_result_df.rename({column: query_object_list[0].fields[column]}, axis=1, inplace=True)
            elif 'exclude' == column:  # 添加到exclude列表，最后统一删除。
                exclude_list.append(column)
            elif ('+' in column) or ('-' in column) or ('*' in column) or ('/' in column):  # 表达式
                var_list = list(set(RestSQL._extract_var(column)))
                for var in var_list:
                    column = column.replace(var, 'data_frame[\'{}\']'.format(var))
                try:
                    main_result_df[query_object_list[0].fields[column]] = eval(column)
                except:
                    raise RunningException(1, '计算 %s : %s 时出错', column, sys.exc_info()[0])
            else:
                main_result_df.drop(column, axis=1, inplace=True)
        for column in exclude_list:  # 删除exclude部分
            main_result_df.drop(column, axis=1, inplace=True)
        return main_result_df

    @staticmethod
    def _query_by_same_source(query_object, engine, conn):
        """
        执行同源的query查询。
        注意，请保证attach到main query的sub query与main query同源。
        :param query_object:
        :param engine:
        :param conn:
        :return:
        """
        if issubclass(type(engine), Engine):
            query, params, fields = engine.parse_object(query_object)
            result_df = engine.fetch_result(conn, query, params, fields)  # Dataframe of result
            return result_df
        else:
            raise ProgramConfigException(401, '请联系开发者，query by same source参数错误。需要Engine，而不是%s。', type(engine))

    @staticmethod
    def _extract_var(expression):
        """
        将计算表达式中的变量提取出来
        :param expression:  (a+b)*(c-d)
        :return: [a,b,c,d]
        """
        return re.findall('[^\+,\-,\*,\/,(,)]+', expression)

# -*- coding: utf-8 -*-
# @Time : 2022/7/10 14:25
# @Author : XXX
# @Site : 
# @File : filter.py
# @Software: PyCharm
import re

def text_to_nums(text: str, count: int):
    """
    将彩票号码文本转换成数字列表
    """
    nums_list = []  # 数字列表
    for idx, line in enumerate(text.split('\n')):
        # 正则匹配字符串
        pattern = (r'\d{1,2}\s+')*(count - 1) + (r'\d{1,2}\s*')
        result = re.search(pattern, line)
        # 无匹配模式的字符串
        if result is None:
            return {'code': -1, 'data': idx}
        # 号码按空格分隔
        nums = line.split(' ')
        # 防止用户意外输入空格
        while(nums.count('')):
            nums.remove('')
        # 判断输入的号码个数是否和彩票类型相符
        if len(set(nums)) != count:
            return {'code': -2, 'data': idx}
        else:
            nums_list.append(nums)
    return {'code': 1, 'data': nums_list}


def compare_lottery_nums(lottery_nums_a: list, lottery_nums_b: list):
    """
    彩票号码对比
    """
    lottery_nums_a = [int(a) for a in lottery_nums_a]
    lottery_nums_b = [int(b) for b in lottery_nums_b]
    duplicate = 0
    # 比较彩票号码
    for num in lottery_nums_a:
        duplicate += 1 if num in lottery_nums_b else 0
    return duplicate  # 返回重复的个数


def match_all(lottery_nums, lottery_nums_group, left, right):
    """
    lottery_nums 是否与 lottery_nums_group 中每组号码全部匹配
    """
    for nums in lottery_nums_group:
        duplicate = compare_lottery_nums(lottery_nums, nums)
        # 如果存在不满足条件的号码，则直接返回False
        if duplicate < left or duplicate > right:
            return False
    return True


def match_any(lottery_nums, lottery_nums_group, left, right):
    """
    lottery_nums 是否与 lottery_nums_group 中某组号码匹配
    """
    for nums in lottery_nums_group:
        duplicate = compare_lottery_nums(lottery_nums, nums)
        # 如果存在满足条件的号码，则直接返回True
        if duplicate >= left and duplicate <= right:
            return True
    return False


def outer_filter_all(lottery_nums_group_a: list, lottery_nums_group_b: list, left: int, right: int):
    """
    外部过滤，且A中一组号码与B中每组号码都重复 left - right 个号码
    """
    match_result = []  # 过滤结果
    mismatch_result = []  # 未过滤结果

    # 遍历A
    for nums_a in lottery_nums_group_a:
        # 如果该组号码与 B 中每组号码都重复 left-right 个号，则加入到结果列表中
        if match_all(nums_a, lottery_nums_group_b, left, right):
            match_result.append(nums_a)
        else:
            mismatch_result.append(nums_a)

    # 返回过滤结果
    return match_result, mismatch_result


def outer_filter_any(lottery_nums_group_a: list, lottery_nums_group_b: list, left: int, right: int):
    """
    外部过滤，且A中一组号码与B中任意一组号码都重复duplicate个号码
    """
    match_result = []  # 过滤结果
    mismatch_result = []  # 未过滤结果

    # 遍历A
    for nums_a in lottery_nums_group_a:
        # 如果该组号码与 B 中任意一组号码重复 left-right 个号，则加入到结果列表中
        if match_any(nums_a, lottery_nums_group_b, left, right):
            match_result.append(nums_a)
        else:
            mismatch_result.append(nums_a)

    # 返回过滤结果
    return match_result, mismatch_result


def inner_filter_any(lottery_nums_group: list, left: int, right: int):
    """
    每组内部过滤
    """
    n = len(lottery_nums_group)  # 总的号码组数
    match_result = []  # 过滤结果
    mismatch_result = []  # 未过滤结果

    # 遍历号码组
    for idx, nums in enumerate(lottery_nums_group):
        other_nums = lottery_nums_group[0: idx] + lottery_nums_group[idx + 1: n]  # 除当前号码外的其他组号码
        if match_any(nums, other_nums, left, right):
            match_result.append(nums)
        else:
            mismatch_result.append(nums)

    # 返回过滤结果
    return match_result, mismatch_result


def prize_analysize(filter_nums_group: list, prize_nums: list):
    """
    对过滤后的彩票号码进行中奖分析
    """
    # 中奖分析结果
    analysis_result = {idx: [] for idx in range(len(prize_nums) + 1)}

    for idx, nums in enumerate(filter_nums_group):
        duplicate = compare_lottery_nums(nums, prize_nums)
        analysis_result[duplicate].append({
            'id': idx,
            'nums': nums
        })

    return analysis_result


if __name__ == '__main__':
    group_a = [
        [1, 2, 3, 4, 5, 7],
        [2, 3, 4, 5, 6, 7]
    ]
    group_b = [
        [3, 4, 5, 6, 7, 8],
        [2, 4, 6, 8, 10, 12],

        [2, 3, 5, 6, 7, 12]
    ]
    # match_result, mismatch_result = outer_filter_all(group_b, group_a, 4, 5)
    # match_result, mismatch_result = outer_filter_any(group_b, group_a, 4, 5)
    # match_result, mismatch_result = inner_filter_any(group_b, 4, 5)
    # analysis_result = prize_analysize(group_b, [0, 1, 2, 3, 4, 5])
    # print(match_result)
    # print(mismatch_result)
    # print(analysis_result)

    # text = '01 02 03 04  05 06'
    # print(text_to_nums_list(text, 6))
    # print(text.split(' '))
    # print(type(None))

    text1 = '1 2 3 4 5 6 7\n'
    text2 = '02 04 06 08 10 12 14\n01 02 03 04 05 06 08\n04 05 07 08 09 14 23\n03 04 13 15 18 19 24'
    group_a = text_to_nums(text1, 7)
    print(group_a)
    # group_b = text_to_nums(text2, 7)['data']
    # match_result, dismatch_result = inner_filter_any(group_a, 4, 7)
    # match_result, dismatch_result = inner_filter_any(group_b, 4, 7)
    # match_result, dismatch_result = outer_filter_all(group_a, group_b, 0, 3)
    # match_result, dismatch_result = outer_filter_all(group_b, group_a, 0, 3)
    # match_result, dismatch_result = outer_filter_any(group_a, group_b, 5, 7)
    # match_result, dismatch_result = outer_filter_any(group_b, group_a, 5, 7)
    # print('match: ', match_result)
    # print('dismatch: ', dismatch_result)
    # result = prize_analysize(match_result, ['01', '02', '03', '04', '05', '06', '07'])
    # print(result)
# -*- coding: utf-8 -*-
# @Time : 2022/7/10 14:25
# @Author : XXX
# @Site : 
# @File : filter.py
# @Software: PyCharm
import re
import itertools


def match_line(text: str, count: int):
    """
    是否匹配
    :param count:
    :param text:
    :return:
    """
    pattern = r'\d{2}\s' * (count - 1) + r'\d{2}'
    # 正则匹配字符串
    return re.search(pattern, text)


def text_to_nums(text: str, count: int):
    """
    将彩票号码文本转换成数字列表
    """
    nums_list = []  # 数字列表
    for idx, line in enumerate(text.split('\n')):
        result = match_line(line, count)
        if result is None:
            return {'flag': False, 'data': idx}
        else:
            nums_list.append(result.group().split(' '))
    return {'flag': True, 'data': nums_list}


def compare_lottery_nums(lottery_nums_a: list, lottery_nums_b: list):
    """
    彩票号码对比
    """
    # 返回重复的个数
    return len(set(lottery_nums_a) & set(lottery_nums_b))


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
        if left <= duplicate <= right:
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
        other_nums = lottery_nums_group[idx + 1: n] + lottery_nums_group[0: idx]  # 除当前号码外的其他组号码
        if match_any(nums, other_nums, left, right):
            match_result.append(nums)
        else:
            mismatch_result.append(nums)

    # 返回过滤结果
    return match_result, mismatch_result


def gen_inner_all(lottery_nums_group, total_count, prize_count, left, right):
    """
    根据已有号码生成
    :return:
    """
    all_nums = [('0' if idx < 9 else '') + str(idx + 1) for idx in range(total_count)]
    # 所有组合
    all_combinations = list(itertools.combinations(all_nums, prize_count))
    match_result, mismatch_result = outer_filter_all(all_combinations, lottery_nums_group, left, right)
    return match_result, mismatch_result


def count_nums(filter_results, total_count):
    """
    统计过滤结果中每个号码出现的次数
    """
    count_dict = {}  # 记录号码出现次数的字典
    # 所有号码
    lottery_nums = [('0' if idx < 9 else '') + str(idx + 1) for idx in range(total_count)]
    # 展开列表
    nums_flat = [num for nums in filter_results for num in nums]
    # 求所有号码出现的次数
    for lottery_num in lottery_nums:
        count_dict[lottery_num] = nums_flat.count(lottery_num)
    return count_dict


def prize_analysize(filter_nums_group: list, prize_nums: list):
    """
    对过滤后的彩票号码进行中奖分析
    """
    # 中奖分析结果
    analysis_result = {idx: [] for idx in range(len(prize_nums) + 1)}

    for idx, nums in enumerate(filter_nums_group):
        duplicate = compare_lottery_nums(nums, prize_nums)
        analysis_result[duplicate].append({
            'id': idx + 1,
            'nums': nums
        })

    return analysis_result


if __name__ == '__main__':
    fa = open('data/a.txt', mode='r')
    fb = open('data/b.txt', mode='r')
    text_a = fa.read().strip().strip('\n')
    text_b = fb.read().strip().strip('\n')
    nums_a = text_to_nums(text_a, 7)['data']
    nums_b = text_to_nums(text_b, 7)['data']
    # match_result, mismatch_result = gen_inner_all(nums_a, 24, 7, 1, 7)
    # match_result, mismatch_result = gen_inner_all(nums_b, 24, 7, 0, 7)

    fa.close()
    fb.close()
    print(count_nums(nums_a, 24))

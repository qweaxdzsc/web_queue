#!/usr/bin/env python
# _*_coding:utf-8_*_
from django.utils.safestring import mark_safe


class PageInfo(object):
    def __init__(self, current, totalItem, peritems=5):
        self.__current = current
        self.__peritems = peritems
        self.__totalItem = totalItem

    def From(self):
        return (self.__current - 1) * self.__peritems

    def To(self):
        return self.__current * self.__peritems

    def TotalPage(self):  # 总页数
        result = divmod(self.__totalItem, self.__peritems)
        if result[1] == 0:
            return result[0]
        else:
            return result[0] + 1


def Custompager(baseurl, currentPage, totalpage):  # 基础页，当前页，总页数
    perPager = 11
    # 总页数<11
    # 0 -- totalpage
    # 总页数>11
    # 当前页大于5 currentPage-5 -- currentPage+5
    # currentPage+5是否超过总页数,超过总页数，end就是总页数
    # 当前页小于5 0 -- 11
    begin = 0
    end = 0
    if totalpage <= 11:
        begin = 0
        end = totalpage
    else:
        if currentPage > 5:
            begin = currentPage - 5
            end = currentPage + 5
            if end > totalpage:
                end = totalpage
        else:
            begin = 0
            end = 11
    pager_list = []
    if currentPage <= 1:
        first = "<a href=''>首页</a>"
    else:
        first = "<a href='%s%d'>首页</a>" % (baseurl, 1)
    pager_list.append(first)

    if currentPage <= 1:
        prev = "<a href=''>上一页</a>"
    else:
        prev = "<a href='%s%d'>上一页</a>" % (baseurl, currentPage - 1)
    pager_list.append(prev)

    for i in range(begin + 1, end + 1):
        if i == currentPage:
            temp = "<a href='%s%d' class='selected'>%d</a>" % (baseurl, i, i)
        else:
            temp = "<a href='%s%d'>%d</a>" % (baseurl, i, i)
        pager_list.append(temp)
    if currentPage >= totalpage:
        next = "<a href='#'>下一页</a>"
    else:
        next = "<a href='%s%d'>下一页</a>" % (baseurl, currentPage + 1)
    pager_list.append(next)
    if currentPage >= totalpage:
        last = "<a href=''>末页</a>"
    else:
        last = "<a href='%s%d'>末页</a>" % (baseurl, totalpage)
    pager_list.append(last)
    result = ''.join(pager_list)
    return mark_safe(result)  # 把字符串转成html语言


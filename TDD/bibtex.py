def extract_author(strData):
    """
    此函数用于从单个作者字符串中提取姓氏和名字。

    :param strData: 包含单个作者姓名信息的字符串
    :return: 包含姓氏和名字的元组，格式为 (姓氏, 名字)
    """
    # 若字符串中存在逗号，表明可能是“姓氏, 名字”格式
    if ',' in strData:
        # 以逗号为分隔符将字符串拆分成多个部分
        strDataParts = strData.split(',')
        # 提取姓氏部分，去除首尾空格
        surname = strDataParts[0].strip()
        # 提取名字部分，将逗号后的所有部分连接起来并去除首尾空格
        forenames = ''.join(strDataParts[1:]).strip()
    # 若字符串中存在空格，表明可能是“名字 姓氏”或“名字 中间名 姓氏”格式
    elif ' ' in strData:
        # 以空格为分隔符拆分字符串
        strDataParts = strData.split(' ')
        # 如果拆分后的部分数量大于 2，说明可能是“名字 中间名 姓氏”格式
        if len(strDataParts) > 2:
            # 连接前两个部分作为名字，去除首尾空格
            forenames = ' '.join(strDataParts[:2]).strip()
            # 连接剩余部分作为姓氏，去除首尾空格
            surname = ','.join(strDataParts[2:]).strip()
        # 如果拆分后的部分数量为 2，说明是“名字 姓氏”格式
        else:
            forenames = strDataParts[0].strip()
            surname = ''.join(strDataParts[1:]).strip()
    # 若字符串中既无逗号也无空格，将整个字符串视为姓氏，名字部分为空
    else:
        surname = strData.strip()
        forenames = ''

    return surname, forenames


def extract_authors(strData):
    """
    此函数用于从包含多个作者姓名的字符串中提取所有作者的姓氏和名字列表。

    :param strData: 包含多个作者姓名，以“and”分隔的字符串
    :return: 包含所有作者姓名对的列表，每个姓名对格式为 (姓氏, 名字)
    """
    # 以“and”为分隔符拆分字符串，得到单个作者字符串的列表
    authors = strData.split(' and ')
    # 对每个作者字符串调用 extract_author 函数提取姓名对，并组成列表返回
    return [extract_author(author) for author in authors]
def is_chinese(uchar):
    if (uchar >= u'\U00004e00' and uchar <= u'\U00009fa5') or \
        (uchar >= u'\U00010000' and uchar <= u'\U0002ffff'):
        return True
    else:
        return False

def is_simple_chinese(uchar):
    if (uchar >= u'\U00004e00' and uchar <= u'\U00009fa5'):
        return True
    else:
        return False

from .constants import *

class node():

    def __init__(self, idx, head, form, feats = None, span = None):

        self.idx = idx
        self.head = head
        self.span = span
        self.form = form
        self.feats = feats
        self.state = False

    def __repr__(self):

        out = "node[%d] = {head: %s, " % (self.idx, self.head)

        if self.span:
            out += "span: %s, " % (self.span,)

        if type(self.form) == str:
            out += "form: %s, " % self.form

        out += "feats: %s}" % (self.feats or "{}")

        if type(self.form) == list:
            for i, form in enumerate(self.form):
                out += "\n  %s" % form

        return out

def printl(*args, **kwargs):
    print(*args, **kwargs, file = LOG_FILE_STREAM)

def final_consonant(c):

    fc = "ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ"
    num = "영일이삼사오육칠팔구"

    if c in "0123456789":
        c = num[int(c)]

    u = ord(c)
    if u < 0xAC00 or u > 0xD7A3:
        return None

    u = (u - 0xAC00) % 28

    return fc[u - 1] if u else None

def realize_ko_morpheme(prev, x):

    if prev in (None, " "):
        return x

    fc = final_consonant(prev)

    if x == "와":
        return "과" if fc else "와"
    if x == "으로":
        return "로" if fc in (None, "ㄹ") else x
    if x == "은":
        return x if fc else "는"
    if x == "을":
        return x if fc else "를"
    if x == "이":
        return x if fc else "가"
    if x == "이다":
        return x if fc else "이다"
    if x == "이라고":
        return x if fc else "이라고"
    if x == "이라는":
        return x if fc else "이라는"
    if x == "이랑":
        return x if fc else "랑"
    if x == "이에요":
        return x if fc else "예요"

    return x

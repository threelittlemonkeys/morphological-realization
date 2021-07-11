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

def realize_ko_morpheme(prev, uf):

    if prev in (None, " "):
        return uf

    fc = final_consonant(prev)

    if uf == "와": return "과" if fc else "와"
    if uf == "으로": return "로" if fc in (None, "ㄹ") else uf
    if uf == "은": return uf if fc else "는"
    if uf == "을": return uf if fc else "를"
    if uf == "이": return uf if fc else "가"
    if uf == "이다": return uf if fc else "이다"
    if uf == "이라고": return uf if fc else "이라고"
    if uf == "이라는": return uf if fc else "이라는"
    if uf == "이랑": return uf if fc else "랑"
    if uf == "이에요": return uf if fc else "예요"

    return uf

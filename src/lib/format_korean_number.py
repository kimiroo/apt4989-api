def format_korean_number(clean_num: str) -> str:
    '''
    숫자만 있는 문자열을 한국 표준 전화번호 형식(하이픈)으로 변환합니다.
    '''
    # 1. 서울 지역번호 (02) - 9~10자리
    if clean_num.startswith('02'):
        if len(clean_num) == 9: # 02-123-4567
            return f'{clean_num[:2]}-{clean_num[2:5]}-{clean_num[5:]}'
        if len(clean_num) == 10: # 02-1234-5678
            return f'{clean_num[:2]}-{clean_num[2:6]}-{clean_num[6:]}'

    # 2. 일반 지역번호/휴대폰 (010, 031, 070 등) - 10~11자리
    if len(clean_num) == 10: # 031-123-4567
        return f'{clean_num[:3]}-{clean_num[3:6]}-{clean_num[6:]}'
    if len(clean_num) == 11: # 010-1234-5678
        return f'{clean_num[:3]}-{clean_num[3:7]}-{clean_num[7:]}'

    return clean_num # 형식이 맞지 않으면 원본 반환

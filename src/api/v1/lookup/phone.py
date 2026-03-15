import re

from fastapi import APIRouter, Depends, Query
from typing import Annotated

from lib.schema.property import Property
from lib.deps import get_mdb
from lib.db import MDBManager
from lib.format_korean_number import format_korean_number
from lib.gen_response_obj import gen_response_obj


router = APIRouter()

@router.get('/phone')
def lookup_phone(
        number: Annotated [
            str,
            Query(
                ...,
                title='전화번호',
                description='조회할 전화번호',
                min_length=4,
                max_length=20,
            )
        ],
        complex: Annotated [
            str | None,
            Query(
                title='단지',
                description='검색 범위를 해당 단지로 제한',
                min_length=1,
                max_length=20
            )
        ] = None,
        mdb: MDBManager = Depends(get_mdb)
    ):

    # Extract numbers
    clean_num = ''.join(filter(str.isdigit, number))

    # Check Korean phone number
    is_korean = re.fullmatch(r'\d{2,3}(?:-|)\d{3,4}(?:-|)\d{4}', clean_num)

    search_targets = [f'%{clean_num}%']

    if is_korean:
        hyphen_num = format_korean_number(clean_num)
        if hyphen_num != clean_num:
            search_targets.append(f'%{hyphen_num}%')
    else:
        if number not in search_targets:
            search_targets.append(f'%{number}%')

    # Base search query
    # search_targets (e.g. ['%01012345678%', '%010-1234-5678%'])
    # S30 - Owner, S33 - Tenant
    conditions = ['(S30 LIKE ? OR S30 LIKE ? OR S33 LIKE ? OR S33 LIKE ?)']
    params = list(search_targets * 2)

    # Add complex to the query if provided
    if complex:
        conditions = ['(S1 LIKE ?)'] + conditions
        params = [f'%{complex}%'] + params

    sql = f'''
        SELECT *
        FROM MAIN
        WHERE {' AND '.join(conditions)}
    '''

    raw_results = mdb.query(sql, tuple(params))
    processed_results = [Property(**row) for row in raw_results]

    result = [gen_response_obj(x) for x in processed_results]

    return result
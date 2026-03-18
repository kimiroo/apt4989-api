from fastapi import APIRouter, Depends, Query
from typing import Annotated

from lib.schema.property import Property
from lib.deps import get_mdb
from lib.db import MDBManager
from lib.gen_response_obj import gen_response_obj


router = APIRouter()

@router.get('/keyword')
def lookup_keyword(
        keyword: Annotated [
            str,
            Query(
                ...,
                title='텍스트',
                description='검색할 텍스트',
                min_length=1,
                max_length=32
            )
        ],
        complex: Annotated [
            str | None,
            Query(
                title='단지',
                description='검색 대상 단지',
                min_length=1,
                max_length=20
            )
        ] = None,
        bld: Annotated [
            str | None,
            Query(
                title='동',
                description='검색 대상 동',
                min_length=1,
                max_length=20
            )
        ] = None,
        listing_only: Annotated [
            bool,
            Query(
                title='거래 상태만 검색',
                description='매매, 전세, 월세 상태만 검색할지 여부'
            )
        ] = False,
        mdb: MDBManager = Depends(get_mdb)
    ):

    # 1. Common target columns
    target_columns = [
        'S17', # 매매
        'S18', # 전세
        'S19'  # 월세
    ]

    # Add target columns if not listing_only
    if not listing_only:
        target_columns.extend([
            'S25', # 확장
            'S26', # 붙박이
            'S28', # 상담
            'S29', # 임대인
            'S32', # 임차인
            'S36'  # 비고
        ])

    # 2. Dynamic SQL query creation
    conditions = [f'TRIM({col}) LIKE ?' for col in target_columns]
    params = [f'%{keyword.strip()}%'] * len(target_columns)

    conditions_filter = []
    conditions_filter_sql = ''

    if bld:
        conditions_filter = ['(TRIM(S3) = ?)']
        params = [bld.strip()] + params

    if complex:
        conditions_filter = ['(TRIM(S1) = ?)'] + conditions_filter
        params = [complex.strip()] + params

    if conditions_filter:
        conditions_filter_sql = f'({' AND '.join(conditions_filter)}) AND '

    sql = f'''
        SELECT *
        FROM MAIN
        WHERE {conditions_filter_sql} ({' OR '.join(conditions)})
    '''

    raw_results = mdb.query(sql, tuple(params))
    processed_results = [Property(**row) for row in raw_results]

    result = [gen_response_obj(x) for x in processed_results]

    return result
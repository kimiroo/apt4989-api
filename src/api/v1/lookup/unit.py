from fastapi import APIRouter, Depends, Query
from typing import Annotated

from lib.schema.property import Property
from lib.deps import get_mdb
from lib.db import MDBManager
from lib.gen_response_obj import gen_response_obj


router = APIRouter()

@router.get('/unit')
def lookup_unit(
        complex: Annotated [
            str,
            Query(
                ...,
                title='단지',
                description='검색 대상 단지',
                min_length=1,
                max_length=20
            )
        ],
        bld: Annotated [
            str,
            Query(
                ...,
                title='동',
                description='검색 대상 동',
                min_length=1,
                max_length=20
            )
        ],
        unit: Annotated [
            str | None,
            Query(
                title='호',
                description='검색 대상 호',
                min_length=1,
                max_length=20
            )
        ] = None,
        mdb: MDBManager = Depends(get_mdb)
    ):

    conditions = ['(TRIM(S1) = ?)', '(TRIM(S3) = ?)']
    params = [complex.strip(), bld.strip()]

    if unit:
        conditions.append('(TRIM(S4) = ?)')
        params.append(unit.strip())

    sql = f'''
        SELECT *
        FROM MAIN
        WHERE {' AND '.join(conditions)}
    '''

    raw_results = mdb.query(sql, tuple(params))
    processed_results = [Property(**row) for row in raw_results]

    result = [gen_response_obj(x) for x in processed_results]

    return result
from fastapi import APIRouter, Depends, Query
from typing import Annotated

from lib.deps import get_mdb
from lib.db import MDBManager


router = APIRouter()

@router.get('/units')
def get_unit_names(
        complex: Annotated [
            str,
            Query(
                ...,
                title='단지명',
                description='호수 목록을 불러올 단지명',
                min_length=1,
                max_length=32
            )
        ],
        bld: Annotated [
            str,
            Query(
                ...,
                title='동',
                description='호수 목록을 불러올 동명',
                min_length=1,
                max_length=32
            )
        ],
        mdb: MDBManager = Depends(get_mdb)
    ):
    # 1. Remove duplicates + trim + order by ascending
    sql = """
        SELECT DISTINCT TRIM(S4) AS NAME
        FROM MAIN
        WHERE S1 = ?
          AND S3 = ?
          AND S3 IS NOT NULL
        ORDER BY TRIM(S4) ASC
    """

    raw_results = mdb.query(sql, (complex, bld))

    # 2. convert to str list
    unit_names = [row['NAME'] for row in raw_results if row.get('NAME')]

    return unit_names
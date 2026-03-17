from fastapi import APIRouter, Depends, Query
from typing import Annotated

from lib.deps import get_mdb
from lib.db import MDBManager


router = APIRouter()

@router.get('/complex/buildings')
def get_building_names(
        complex: Annotated [
            str,
            Query(
                ...,
                title='단지명',
                description='동 목록을 불러올 단지명',
                min_length=1,
                max_length=32
            )
        ],
        mdb: MDBManager = Depends(get_mdb)
    ):
    # 1. Remove duplicates + trim + order by ascending
    sql = """
        SELECT DISTINCT TRIM(S3)
        FROM MAIN
        WHERE S1 = ?
          AND S3 IS NOT NULL
        ORDER BY TRIM(S3) ASC
    """

    raw_results = mdb.query(sql, (complex,))

    # 2. convert to str list
    building_names = [row['C1'] for row in raw_results if row.get('C1')]

    return building_names
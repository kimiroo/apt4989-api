from fastapi import APIRouter, Depends

from lib.deps import get_mdb
from lib.db import MDBManager


router = APIRouter()

@router.get('/complexes')
def get_complex_names(mdb: MDBManager = Depends(get_mdb)):
    # 1. Remove duplicates + trim + order by ascending
    sql = "SELECT DISTINCT TRIM(S1) FROM MAIN WHERE S1 IS NOT NULL ORDER BY TRIM(S1) ASC"

    raw_results = mdb.query(sql)

    # 2. convert to str list
    complex_names = [row['C1'] for row in raw_results if row.get('C1')]

    return complex_names
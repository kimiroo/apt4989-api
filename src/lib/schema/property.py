from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class Property(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,    # 변수명(complex)으로 생성 가능
        serialize_by_alias=False  # 출력할 때 별칭(S1) 무시
    )

    complex: str = Field(..., alias='S1')
    bld: str = Field(..., alias='S3')
    unit: str = Field(..., alias='S4')

    area: Optional[str] = Field(None, alias='S2')
    type: Optional[str] = Field(None, alias='S5')

    # Owner
    owner_name: Optional[str] = Field(None, alias='S29')
    owner_number: Optional[str] = Field(None, alias='S30')

    # Tenant
    tenant_name: Optional[str] = Field(None, alias='S32')
    tenant_number: Optional[str] = Field(None, alias='S33')

    # Sale
    sale_state: Optional[str] = Field(None, alias='S17')
    sale_price: Optional[str] = Field(None, alias='S20')

    # Jeonse
    jeonse_state: Optional[str] = Field(None, alias='S18')
    jeonse_price: Optional[str] = Field(None, alias='S21')

    # Rent
    rent_state: Optional[str] = Field(None, alias='S19')
    rent_prices: Optional[str] = Field(None, alias='S23')
    rent_deposits: Optional[str] = Field(None, alias='S22')

    # Expiration date
    expire_yy: Optional[str] = Field(None, alias='S12')
    expire_mm: Optional[str] = Field(None, alias='S13')
    expire_dd: Optional[str] = Field(None, alias='S14')

    @property
    def expiration_date(self) -> str:
        '''Integrates split expiration dates safely or returns status messages.'''
        # 1. Return 'Pending' if the year field is empty or whitespace
        if not self.expire_yy or not self.expire_yy.strip():
            return ''

        # 2. Check if the year field is numeric (Standard date format)
        if self.expire_yy.isdigit():
            # Strip and validate month and day fields
            mm = self.expire_mm.strip() if self.expire_mm else ''
            dd = self.expire_dd.strip() if self.expire_dd else ''

            # Assemble into 'YYYY-MM-DD' if parts are numeric; otherwise, return year only
            date_parts = [self.expire_yy]
            if mm.isdigit():
                date_parts.append(mm.zfill(2))
            if dd.isdigit():
                date_parts.append(dd.zfill(2))

            return '-'.join(date_parts)

        # 3. If the year field is non-numeric (e.g., 'Reserved', 'Negotiating'), return as-is
        return self.expire_yy.strip()

    # Features
    features_1: Optional[str] = Field(None, alias='S25')
    features_2: Optional[str] = Field(None, alias='S26')

    @property
    def features(self) -> list:
        # 인스턴스(self)의 실제 값들을 확인해서 리스트로 만듭니다.
        return [v for v in [self.features_1, self.features_2] if v and v.strip()]

    consult_log: Optional[str] = Field(None, alias='S28')
    remarks: Optional[str] = Field(None, alias='S36')

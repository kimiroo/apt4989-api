from lib.schema.property import Property

def gen_response_obj(property: Property):
    return {
        'complex': property.complex,
        'bld': property.bld,
        'unit': property.unit,
        'area': property.area,
        'type': property.type,
        'owner': {
            'name': property.owner_name,
            'number': property.owner_number
        },
        'tenant': {
            'name': property.tenant_name,
            'number': property.tenant_number
        },
        'listing': {
            'sale': {
                'state': property.sale_state,
                'price': property.sale_price
            },
            'jeonse': {
                'state': property.jeonse_state,
                'price': property.jeonse_price
            },
            'rent': {
                'state': property.rent_state,
                'prices': property.rent_prices,
                'deposits': property.rent_deposits
            }
        },
        'expirationDate': property.expiration_date,
        'features': property.features,
        'consultLog': property.consult_log,
        'remarks': property.remarks
    }
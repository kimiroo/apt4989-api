from lib.schema.property import Property

def map_property(row: dict) -> Property:
    return Property(**row)
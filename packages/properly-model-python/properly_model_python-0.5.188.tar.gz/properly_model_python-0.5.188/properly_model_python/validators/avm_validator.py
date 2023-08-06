BASE_REQUIRED_FEATURES = [
    "address",
    "bedroomsTotal",
    "bathroomsFull",
    "bathroomsTotal",
    "buildingType",
    "enclosedParking",
    "directionFaces",
    "latitude",
    "longitude",
    "parking",
    "style",
    "totalParking",
]

CONDO_ONLY_REQUIRED_FEATURES = [
    "associationFee",
    "bedroomsStandard",
    "buildingPlaceId",
    "unitNumber",
]

RESIDENTIAL_ONLY_REQUIRED_FEATURES = [
    "basement",
    "exterior",
    "heatingType",
]

# TRREB municipalities map - https://www.torontomls.net/Communities/map.html
# properlyMunicipalityCode format - https://github.com/GoProperly/airflow-pipelines/blob/b5a959e64ccbb796f65970477b8772a5e502444d/dags/rets_creb_idx.py#L281
SUPPORTED_MUNICIPALITY_CODES = {
    # Durham - Ajax, Brock, Clarington, Oshawa, Pickering, Scugog, Uxbridge, Whitby
    "ajax-on-ca",
    "brock-on-ca",
    "clarington-on-ca",
    "oshawa-on-ca",
    "pickering-on-ca",
    "scugog-on-ca",
    "uxbridge-on-ca",
    "whitby-on-ca"
    # Halton - Burlington, Halton Hills, Milton, Oakville
    "burlington-on-ca",
    "halton_hills-on-ca",
    "milton-on-ca",
    "oakville-on-ca",
    # Peel - Brampton, Caledon, Mississauga
    "brampton-on-ca",
    "caledon-on-ca",
    "mississauga-on-ca",
    # Toronto
    "toronto-on-ca",
    # York - Aurora, East Gwillimbury, Geogina, King, Markham, Newmarket, Richmond Hill, Whitchurch-Stouville, Vaughan
    "aurora-on-ca",
    "east_gwillimbury-on-ca",
    "georgina-on-ca",
    "king-on-ca",
    "markham-on-ca",
    "newmarket-on-ca",
    "richmond_hill-on-ca",
    "whitchurch_stouffville-on-ca",
    "vaughan-on-ca",
}


def check_property_price_avm_ready(model_property: dict) -> bool:
    """
    Determines whether there is enough data to get a reasonable AVM price estimate
    :param model_property: dictionary of property values in ModelProperty spec
    :return: True if the input contains enough data for a reasonable AVM price estimate
    """
    city_code = model_property.get("properlyCityCode")
    municipality_code = model_property.get("properlyMunicipalityCode")

    # Initially we only support the GTA
    if (
        city_code != "toronto-on-ca"
        or municipality_code not in SUPPORTED_MUNICIPALITY_CODES
    ):
        return False

    if "associationFee" in model_property:
        required_features = BASE_REQUIRED_FEATURES + CONDO_ONLY_REQUIRED_FEATURES
    else:
        required_features = BASE_REQUIRED_FEATURES + RESIDENTIAL_ONLY_REQUIRED_FEATURES

    for feature in required_features:
        if feature not in model_property:
            return False

    return True

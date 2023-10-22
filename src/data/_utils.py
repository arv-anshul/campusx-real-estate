import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

IMPORTANT_INIT_COLS = [
    "PROP_ID",
    "CITY",
    "PRICE",
    "AREA",
    "TOTAL_LANDMARK_COUNT",
    "FORMATTED_LANDMARK_DETAILS",
    "PROP_HEADING",
    "PROPERTY_TYPE",
    "FURNISH",
    "FACING",
    "AGE",
    "BEDROOM_NUM",
    "FEATURES",
    "AMENITIES",
    "PROP_NAME",
    "BALCONY_NUM",
    "FLOOR_NUM",
    "MAP_DETAILS",
    "location",
    "DESCRIPTION",
]

REQUIRED_COLS = [
    "PROP_ID",
    "CITY",
    "PRICE",
    "AREA",
    "PROPERTY_TYPE",
    "FURNISH",
    "FACING",
    "AGE",
    "BEDROOM_NUM",
    "BALCONY_NUM",
    "FLOOR_NUM",
    "LOCALITY_NAME",
    "LUXURY_CATEGORY",
    "PROP_HEADING",
    "DESCRIPTION",
    "PROP_NAME",
    "LATITUDE",
    "LONGITUDE",
    "SOCIETY_NAME",
]

COLS_TO_ESTIMATE_AREA = [
    "BUILTUP_SQFT",
    "CARPET_SQFT",
    "SUPERBUILTUP_SQFT",
    "SUPER_SQFT",
]

FEATURES_MAPPING = {
    "Parking": 5,
    "Park": 7,
    "Power Backup": 9,
    "Lift": 8,
    "Gymnasium": 8,
    "Club house": 7,
    "Waste disposal": 5,
    "Swimming Pool": 8,
    "Security Personnel": 9,
    "Gas Pipeline": 6,
    "Near bank": 5,
    "DG Availability": 7,
    "Wheelchair Accessibility": 4,
    "ATM": 6,
}

AMENITIES_MAPPING = {
    "Waste Disposal": 5,
    "Rain Water Harvesting": 7,
    "Bank Attached Property": 3,
    "Power Back-up": 9,
    "Feng Shui / Vaastu Compliant": 6,
    "Private Garden / Terrace": 8,
    "Centrally Air Conditioned": 9,
    "Security / Fire Alarm": 9,
    "Intercom Facility": 7,
    "Water Storage": 6,
    "Piped-gas": 4,
    "Water purifier": 6,
    "Near Bank": 5,
    "Swimming Pool": 8,
    "Club house / Community Center": 7,
    "Park": 8,
    "Security Personnel": 9,
    "Fitness Centre / GYM": 8,
    "Visitor Parking": 6,
    "Lift(s)": 8,
    "Maintenance Staff": 5,
    "Shopping Centre": 7,
    "WheelChair Accessibilitiy": 4,
    "DG Availability": 7,
    "CCTV Surveillance": 9,
    "Grade A Building": 7,
    "Grocery Shop": 5,
    "ATM": 6,
    "Cafeteria / Food Court": 6,
    "Bar / Lounge": 7,
    "Conference room": 6,
    "Service / Goods Lift": 6,
    "Access to High Speed Internet": 8,
}

LANDMARKS_GROUPS = {
    "TRANSPORTATION": ["station", "bus", "airport"],
    "ACCOMMODATION": ["hotel", "office", "atm", "bank"],
    "OTHER": [
        "religious",
        "connect",
        "miscellaneou",
        "parking",  # Maybe this value is being over-shadowed by `park` in LEISURE.
    ],
    "LEISURE": [
        "shop",
        "mall",
        "park",
        "stadium",
        "club",
        "pool",
        "attraction",
        "golf",
    ],
    "EDUCATION": ["education", "library"],
    "HEALTH": ["hospital", "pharmacy"],
}

COLS_TO_CLUSTER = [
    "TOTAL_LANDMARK_COUNT",
    "TRANSPORTATION",
    "ACCOMMODATION",
    "LEISURE",
    "EDUCATION",
    "HEALTH",
    "OTHER",
    "AMENITIES_SCORE",
    "FEATURES_SCORE",
]


def lookup_mapping(x: list[str], lookup: dict[str, int]) -> float | int:
    if isinstance(x, (float, int)):
        return x

    total_sum = sum(lookup.get(i, 0) for i in x)
    return total_sum


def eval_numeric_values(x: str) -> str | float:
    if pd.isna(x):
        return np.nan

    x = x.replace(".", "")
    if x.isnumeric():
        return int(x)
    return x


def create_LUXURY_CATEGORY(df: pd.DataFrame, n_clusters: int = 3) -> pd.Series:
    scaler = StandardScaler()
    data_ = scaler.fit_transform(df)

    cluster = KMeans(
        n_clusters=n_clusters, init="k-means++", n_init=10, random_state=42
    )

    return pd.Series(cluster.fit_predict(data_), name="LUXURY_CATEGORY")

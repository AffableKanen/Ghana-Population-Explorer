# import pandas as pd
# import geopandas as gp

# DATA = {}

# def load_data():
#     DATA['districts_shapefile'] = gp.read_file(r"apis\data\districts_spatial.geojson")
#     DATA["total_status"] = pd.read_parquet(r'apis\data\disability\total_status.parquet')
#     DATA["seeing"] = pd.read_parquet(r"apis\data\disability\seeing.parquet")
#     DATA["hearing"] = pd.read_parquet(r"apis\data\disability\hearing.parquet")
#     DATA["remembering"] = pd.read_parquet(r"apis\data\disability\remember.parquet")
#     DATA["physical"] = pd.read_parquet(r"apis\data\disability\physical_activity.parquet")
#     DATA["selfcare"] = pd.read_parquet(r"apis\data\disability\selfcare.parquet")
#     DATA["speech"] = pd.read_parquet(r"apis\data\disability\speech.parquet")
#     DATA["child_econ_status"] = pd.read_parquet(r"apis\data\economic\children_economic_status.parquet")
#     DATA["child_econ_industry"] = pd.read_parquet(r"apis\data\economic\economic_active_child_industry.parquet")
#     DATA["econ_active_pop_status"] = pd.read_parquet(r"apis\data\economic\economic_active_population_status.parquet")
#     DATA["econ_active_pop_industry"] = pd.read_parquet(r"apis\data\economic\economic_active_population_industry.parquet")
#     DATA["child_econ_occupation"] = pd.read_parquet(r"apis\data\economic\econ_active_child_occupation.parquet")
#     DATA["econ_active_occupation"] = pd.read_parquet(r"apis\data\economic\econ_active_pop_occupation.parquet")
#     DATA["sector_employment"] = pd.read_parquet(r"apis\data\economic\econ_active_sectors.parquet")
#     DATA["employment_status_classification"] = pd.read_parquet(r"apis\data\economic\employmnet_classification.parquet")
#     DATA["unemployment_rate"] = pd.read_parquet(r"apis\data\economic\unemployment_rate.parquet")
#     DATA["past_attendance"] = pd.read_parquet(r"apis\data\education\past_school_attendance.parquet")


import duckdb
from pathlib import Path
import geopandas as gp
from shapely import wkb

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "apis" / "data" / "ghana_dists.db"

def get_db():
    con = duckdb.connect(DB_PATH, read_only=True)
    con.execute("INSTALL spatial")
    con.execute("LOAD spatial")
    return con

def get_shp(con):
    shp = con.sql("""SELECT *, ST_AsWKB(geom) AS geometry FROM districts""").df()
    shp["geometry"] = shp["geometry"].apply(lambda g: wkb.loads(bytes(g)))
    del shp['geom']
    shp = gp.GeoDataFrame(shp, geometry='geometry', crs="EPSG:4326")
    return shp





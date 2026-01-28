from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from typing import List, Literal, Optional
from apis.data_store import get_db, get_shp

router_past_attendance = APIRouter()

class PastAttendance(BaseModel):
    
    age_column:Literal["All ages",'15-17 years', '18 years & older']
        
    sex:Literal['Both Sexes', 'Male', 'Female']
        
    locality: Literal['All Locality Types','Rural', 'Urban']
        
    education: Literal['Nursery', 'Kindergarten', 'Primary', 'JSS/JHS', 'Middle','SSS/SHS', 'Secondary', 'Voc/technical/commercial',
                       'Post middle/secondary Certificate','Post middle/secondary Diploma', 'Tertiary/HND',"Tertiary - Bachelor's Degree",
                       'Tertiary - Post graduate Certificate/Diploma',"Tertiary - Master's Degree", 'Tertiary - PhD', 'Other (specify)']
    
def get_df(con,age_col, sex, edu, locality):
    if age_col == "All ages":
        df = con.sql(f"""SELECT District,
        "{age_col}" FROM past_school_attendance
        WHERE sex = '{sex}'
        AND locality = '{locality}'
        AND education = '{edu}'
        """).df()
        df = df[['District',age_col]]
        
    else:
        df = con.sql(f"""SELECT District, "All ages",
        "{age_col}" FROM past_school_attendance
        WHERE sex = '{sex}'
        AND locality = '{locality}'
        AND education = '{edu}'
        """).df()
        
        df[age_col] = df[age_col]/df["All ages"] * 100
        df[age_col] = df[age_col].round(1)
        
        df = df[['District',age_col]]
    return df

@router_past_attendance.post("/past_attendance")
@cache(expire=60 * 5)
def get_pastattendance(user_input: PastAttendance):

    con = get_db()

    pastattendance = get_df(con, user_input.age_column, user_input.sex, user_input.education, user_input.locality)

    pastattendance[user_input.age_column] = pastattendance[user_input.age_column].fillna(0)

    pastattendance[user_input.age_column] = pastattendance[user_input.age_column].round(2)
    
    shp = get_shp(con)

    selected = shp.merge(pastattendance, on='District').merge(pastattendance, left_on='Region', right_on='District').drop(['District_y'], axis=1)

    selected = selected.rename(columns={'District_x':'District', f'{user_input.age_column}_x':user_input.age_column, f'{user_input.age_column}_y':'Regional_percentage'})

    selected['National_percentage'] = pastattendance[pastattendance['District']=='Ghana'][user_input.age_column].values[0]

    con.close()

    return selected.to_geo_dict() 
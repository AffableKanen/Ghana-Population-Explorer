from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from typing import List, Literal, Optional
from apis.data_store import get_db, get_shp

router_current_attendance = APIRouter()

class CurrentAttendance(BaseModel):
    
    age_column:Literal['3-5 years','6-14 years', '15-17 years', '18-19 years', '20-24 years', '25-29 years', '30 years & older']
        
    sex:Literal['Both Sexes', 'Male', 'Female']
        
    locality: Literal['All Locality Types','Rural', 'Urban']
        
    education: Literal['Total', 'Nursery', 'Kindergarten', 'Primary', 'JSS/JHS','SSS/SHS', 'Secondary', 'Voc/technical/commercial','Post middle/secondary Certificate',
                       'Post middle/secondary Diploma', 'Tertiary/HND',"Tertiary - Bachelor's Degree",'Tertiary - Post graduate Certificate/Diploma',
                       "Tertiary - Master's Degree", 'Tertiary - PhD', 'Other (specify)']
    
def get_df(con,age_col, sex, edu, locality):
    df = con.sql(f"""SELECT District,
    "{age_col}" FROM current_school_attendance
    WHERE sex = '{sex}'
    AND locality = '{locality}'
    AND education = '{edu}'
    """).df()
    df = df[['District',age_col]]
    return df

@router_current_attendance.post("/current_attendance")
@cache(expire=60 * 5)
def get_currentattendance(user_input: CurrentAttendance):

    con = get_db()

    currentattendance = get_df(con, user_input.age_column, user_input.sex, user_input.education, user_input.locality)

    shp = get_shp(con)

    selected = shp.merge(currentattendance, on='District').merge(currentattendance, left_on='Region', right_on='District').drop(['District_y'], axis=1)

    selected = selected.rename(columns={'District_x':'District', f'{user_input.age_column}_x':user_input.age_column, f'{user_input.age_column}_y':'Regional_percentage'})

    selected['National_percentage'] = currentattendance[currentattendance['District']=='Ghana'][user_input.age_column].values[0]

    con.close()
    return selected.to_geo_dict() 
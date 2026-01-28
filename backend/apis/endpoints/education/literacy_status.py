from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from typing import List, Literal, Optional
from apis.data_store import get_db, get_shp

router_literacy_status = APIRouter()

class LiteracyStatus(BaseModel):
    
    age_column:Literal['All ages', '6-10', '11-14', '15-19', '20-24', '25-29', '30-34','35-39','40-44', '45-49', 
                       '50-54', '55-59', '60-64', '65-69', '70-74','75-79', '80-84', '85-89', '90-94', '95-99', '100+',]
        
    sex:Literal['Both Sexes', 'Male', 'Female']
        
    locality: Literal['All Locality Types','Rural', 'Urban']
        
    education: Literal['Total', 'Never attended', 'Nursery', 'Kindergarten', 'Primary','JSS/JHS', 'Middle', 'SSS/SHS', 'Secondary',
                       'Voc/technical/commercial', 'Post middle/secondary Certificate','Post middle/secondary Diploma', 'Tertiary/HND',
                       "Tertiary - Bachelor's Degree",'Tertiary - Post graduate Certificate/Diploma',"Tertiary - Master's Degree", 'Tertiary - PhD', 'Other (specify)']
    
    status: Literal['Not literate', 'Literate']
    
def get_df(con,age_col, sex, edu, locality):
    df = con.sql(f"""SELECT District,
    "{age_col}", status FROM literacy_status 
    WHERE sex = '{sex}'
    AND locality = '{locality}'
    AND education = '{edu}'
    """).df()
    return df

@router_literacy_status.post("/literacy_status")
@cache(expire=60 * 5)
def get_literacy_status(user_input: LiteracyStatus):

    con = get_db()

    literacystatus = get_df(con, user_input.age_column, user_input.sex, user_input.education, user_input.locality)

    statuses = list(literacystatus['status'].unique())

    literacystatus = literacystatus.pivot(index='District', values=user_input.age_column, columns='status')
    
    literacystatus = literacystatus.div(literacystatus.sum(axis=1), axis=0) * 100

    literacystatus = literacystatus.round(2)
    literacystatus = literacystatus.reset_index()

    literacystatus = literacystatus.melt(id_vars='District', value_vars=statuses, value_name=user_input.age_column)
    
    literacystatus = literacystatus[literacystatus['status']==user_input.status][['District', user_input.age_column]]

    shp = get_shp(con)

    selected = shp.merge(literacystatus, on='District').merge(literacystatus, left_on='Region', right_on='District').drop(['District_y'], axis=1)
    selected = selected.rename(columns={'District_x':'District', f'{user_input.age_column}_x':user_input.age_column, f'{user_input.age_column}_y':'Regional_percentage'})

    selected['National_percentage'] = literacystatus[literacystatus['District']=='Ghana'][user_input.age_column].values[0]

    con.close()
    return selected.to_geo_dict() 
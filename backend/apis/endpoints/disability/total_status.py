from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from typing import List, Literal, Optional
from apis.data_store import get_db, get_shp

router = APIRouter()

class TotalStatus(BaseModel):
    
    age_column:Literal["All_ages",'age_5_9', 'age_10_14', 'age_15_17', 'age_18_19', 'age_20_24','age_25_29', 'age_30_34', 
                        'age_35_39', 'age_40_44', 'age_45_49','age_50_54', 'age_55_59', 'age_60_64', 'age_65_69', 
                        'age_70_74','age_75_79','age_80_84','age_85_89','age_90_94','age_95_99','age_100_plus']
        
    sex:Literal['Both Sexes', 'Male', 'Female']
        
    locality: Literal['All Locality Types','Rural', 'Urban']
        
    education: Literal['Total','Never attended', 'Nursery', 'Kindergarten', 'Primary', 'JSS/JHS','Middle', 'SSS/SHS', 'Secondary', 
                       'Voc/technical/commercial','Post middle/secondary Certificate','Post middle/secondary Diploma', 
                       'Tertiary/HND',"Tertiary - Bachelor's Degree",'Tertiary - Post graduate Certificate/Diploma',
                       "Tertiary - Master's Degree", 'Tertiary - PhD', 'Other (specify)']
        
    # status: Literal['With Difficulty', 'Without Difficulty']
    

@router.post("/total_status")
@cache(expire=60 * 5)
def get_shape(user_input: TotalStatus):

    con = get_db()
    total_status = con.sql(f"""SELECT District,
                "{user_input.age_column}",
                status
                FROM total_status
                WHERE sex = '{user_input.sex}'
                AND locality = '{user_input.locality}'
                AND education = '{user_input.education}'
                """).df()
    
    shp = get_shp(con)
    
    total_status = total_status[total_status['status']=='With Difficulty'][['District', user_input.age_column]].merge(
        total_status[total_status['status']=='Without Difficulty'][['District', user_input.age_column]], on='District')
    
    total_status['percentage'] = total_status.apply(lambda x: (x[user_input.age_column+'_x']/(x[user_input.age_column+'_x']+x[user_input.age_column+'_y']))*100 
                                                  if x[user_input.age_column+'_x']>0 else 0, axis=1)
    
    total_status['percentage'] = total_status['percentage'].round(2)
    
    total_status = total_status[['District', 'percentage']]

    selected = shp.merge(total_status, on='District').merge(total_status, left_on='Region', right_on='District').drop('District_y', axis=1)
    selected = selected.rename(columns={'District_x':'District', 'percentage_x': user_input.age_column, 'percentage_y': 'Regional_percentage'})
    selected['National_percentage'] = total_status[total_status['District']=='Ghana']['percentage'].values[0]

    con.close()

    return selected.to_geo_dict()
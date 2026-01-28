from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from typing import List, Literal, Optional
from apis.data_store import get_db, get_shp

router_speech = APIRouter()

class Speech(BaseModel):
    
    age_column:Literal["All_ages",'age_5_9', 'age_10_14', 'age_15_17', 'age_18_19', 'age_20_24','age_25_29', 'age_30_34', 
                        'age_35_39', 'age_40_44', 'age_45_49','age_50_54', 'age_55_59', 'age_60_64', 'age_65_69', 
                        'age_70_74','age_75_79','age_80_84','age_85_89','age_90_94','age_95_99','age_100+']
        
    sex:Literal['Both Sexes', 'Male', 'Female']
        
    locality: Literal['All Locality Types','Rural', 'Urban']
        
    education: Literal['Total','Never attended', 'Nursery', 'Kindergarten', 'Primary', 'JSS/JHS','Middle', 'SSS/SHS', 'Secondary', 
                       'Voc/technical/commercial','Post middle/secondary Certificate','Post middle/secondary Diploma', 
                       'Tertiary/HND',"Tertiary - Bachelor's Degree",'Tertiary - Post graduate Certificate/Diploma',
                       "Tertiary - Master's Degree", 'Tertiary - PhD', 'Other (specify)']
        
    status: Literal["Cannot communicate at all", "Yes, some difficulty", "Yes, a lot of difficulty", "No difficulty"]
    

@router_speech.post("/speech")
@cache(expire=60 * 5)
def get_speech(user_input: Speech):
    
    con = get_db()
    speech = con.sql(f"""SELECT District,
                "{user_input.age_column}",
                status
                FROM speech
                WHERE sex = '{user_input.sex}'
                AND locality = '{user_input.locality}'
                AND education = '{user_input.education}'
                """).df()
    
    shp = get_shp(con)
    
    statuses = list(speech['status'].unique())

    speech = speech.pivot(index='District', values=user_input.age_column, columns='status')
    
    speech = speech.div(speech.sum(axis=1), axis=0) * 100

    speech = speech.round(2)

    speech = speech.reset_index()

    speech = speech.melt(id_vars='District', value_vars=statuses, value_name=user_input.age_column)
    
    speech = speech[speech['status']==user_input.status][['District', user_input.age_column]]

    selected = shp.merge(speech, on='District').merge(speech, left_on='Region', right_on='District').drop(['District_y'], axis=1)

    selected = selected.rename(columns={'District_x':'District', f'{user_input.age_column}_x':user_input.age_column, f'{user_input.age_column}_y':'Regional_percentage'})

    selected['National_percentage'] = speech[speech['District']=='Ghana'][user_input.age_column].values[0]
    
    con.close()

    return selected.to_geo_dict() 
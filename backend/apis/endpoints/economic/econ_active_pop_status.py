from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from typing import List, Literal, Optional
from apis.data_store import get_db, get_shp

router_econactivestatus = APIRouter()

class EconActiveStatus(BaseModel):
    
    age_column:Literal[ "Total","15-19","20-24","25-29", "30-34", "35-39", "40-44", "45-49","50-54","55-59", "60-64","65-69","70-74","75-79",
                       "80-84", "85-89", "90-94","95-99","100+"]
        
    sex:Literal['Both Sexes', 'Male', 'Female']
        
    locality: Literal['All Locality Types','Rural', 'Urban']
        
    education: Literal["Total","Never attended","Nursery","Kindergarten", "Primary","JSS/JHS","Middle", "SSS/SHS","Secondary","Voc/technical/commercial",
                       "Post middle/secondary Certificate","Post middle/secondary Diploma","Tertiary/HND","Tertiary - Bachelor's Degree","Tertiary - Post graduate Certificate/Diploma",
                       "Tertiary - Master's Degree","Tertiary - PhD", "Other (specify)"]
        
    economic_status: Literal["Employed","Worked","Did not work but had a job","Unemployed","Available but not seeking work","First time job seeker", 
                           "Worked previously & seeking work", "Outside Labour Force"]
    

@router_econactivestatus.post("/econ_active_status")
@cache(expire=60 * 5)
def get_econactivestatus(user_input: EconActiveStatus):

    con = get_db()
    econactivestatus = con.sql(f"""SELECT District,
                "{user_input.age_column}",
                economic_status
                FROM economic_active_population_status
                WHERE sex = '{user_input.sex}'
                AND locality = '{user_input.locality}'
                AND education = '{user_input.education}'
                """).df()
    
    shp = get_shp(con)
    
    statuses = list(econactivestatus['economic_status'].unique())

    econactivestatus = econactivestatus.pivot(index='District', values=user_input.age_column, columns='economic_status')
    
    econactivestatus = econactivestatus.div(econactivestatus.sum(axis=1), axis=0) * 100

    econactivestatus = econactivestatus.round(2)

    econactivestatus = econactivestatus.reset_index()

    econactivestatus = econactivestatus.melt(id_vars='District', value_vars=statuses, value_name=user_input.age_column)
    
    econactivestatus = econactivestatus[econactivestatus['economic_status']==user_input.economic_status][['District', user_input.age_column]]

    selected = shp.merge(econactivestatus, on='District').merge(econactivestatus, left_on='Region', right_on='District').drop(['District_y'], axis=1)

    selected = selected.rename(columns={'District_x':'District', f'{user_input.age_column}_x':user_input.age_column, f'{user_input.age_column}_y':'Regional_percentage'})

    selected['National_percentage'] = econactivestatus[econactivestatus['District']=='Ghana'][user_input.age_column].values[0]

    con.close()

    return selected.to_geo_dict() 
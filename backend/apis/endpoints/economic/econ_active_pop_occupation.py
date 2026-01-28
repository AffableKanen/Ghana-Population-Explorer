from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from typing import List, Literal, Optional
from apis.data_store import get_db, get_shp

router_econactiveoccupation = APIRouter()

class EconActiveOccupation(BaseModel):
    
    age_column:Literal["All ages","15-19","20-24","25-29","30-34","35-39","40-44","45-49",
                       "50-54","55-59","60-64","65-69","70-74","75-79","80-84","85-89","90-94"]
        
    sex:Literal['Both Sexes', 'Male', 'Female']
        
    locality: Literal['All Locality Types','Rural', 'Urban']
        
    education: Literal["Total","Never attended","Nursery","Kindergarten","Primary","JSS/JHS","Middle","SSS/SHS","Secondary",
                       "Voc/technical/commercial","Post middle/secondary Certificate","Post middle/secondary Diploma", "Tertiary/HND",
                       "Tertiary - Bachelor's Degree","Tertiary - Post graduate Certificate/Diploma","Tertiary - Master's Degree",
                       "Tertiary - PhD", "Other (specify)"]
        
    occupations: Literal["Managers","Professionals","Technicians and associate professionals","Clerical support workers","Service and sales workers",
                          "Skilled agricultural, forestry and fishery workers", "Craft and related trades workers","Plant and machine operators, and assemblers",
                          "Elementary occupation workers", "Other occupations"]
    

@router_econactiveoccupation.post("/econ_active_occupation")
@cache(expire=60 * 5)
def get_econactiveoccupation(user_input: EconActiveOccupation):

    con = get_db()
    econactiveoccupation = con.sql(f"""SELECT District,
                "{user_input.age_column}",
                occupations
                FROM econ_active_pop_occupation
                WHERE sex = '{user_input.sex}'
                AND locality = '{user_input.locality}'
                AND education = '{user_input.education}'
                """).df()
    
    shp = get_shp(con)
    
    occupations = list(econactiveoccupation['occupations'].unique())

    econactiveoccupation = econactiveoccupation.pivot(index='District', values=user_input.age_column, columns='occupations')
    
    econactiveoccupation = econactiveoccupation.div(econactiveoccupation.sum(axis=1), axis=0) * 100

    econactiveoccupation = econactiveoccupation.round(2)

    econactiveoccupation = econactiveoccupation.reset_index()

    econactiveoccupation = econactiveoccupation.melt(id_vars='District', value_vars=occupations, value_name=user_input.age_column)
    
    econactiveoccupation = econactiveoccupation[econactiveoccupation['occupations']==user_input.occupations][['District', user_input.age_column]]

    selected = shp.merge(econactiveoccupation, on='District').merge(econactiveoccupation, left_on='Region', right_on='District').drop(['District_y'], axis=1)

    selected = selected.rename(columns={'District_x':'District', f'{user_input.age_column}_x':user_input.age_column, f'{user_input.age_column}_y':'Regional_percentage'})

    selected['National_percentage'] = econactiveoccupation[econactiveoccupation['District']=='Ghana'][user_input.age_column].values[0]

    con.close()

    return selected.to_geo_dict() 
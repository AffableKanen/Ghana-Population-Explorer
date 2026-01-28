from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from typing import List, Literal, Optional
from apis.data_store import get_db, get_shp

router_childeconoccupation = APIRouter()

class ChildEconOccupation(BaseModel):
    
    age_column:Literal["All ages",'5-9', '10-14']
        
    sex:Literal['Both Sexes', 'Male', 'Female']
        
    locality: Literal['All Locality Types','Rural', 'Urban']
        
    education: Literal['Total', 'Never attended', 'Nursery', 'Kindergarten', 'Primary','JSS/JHS', 'SSS/SHS', 'Secondary', 'Voc/technical/commercial']
        
    occupations: Literal["Service and sales workers","Skilled agricultural, forestry and fishery workers","Craft and related trades workers",
                         "Plant and machine operators, and assemblers", "Elementary occupation workers"]
    

@router_childeconoccupation.post("/child_econ_occupation")
@cache(expire=60 * 5)
def get_childeconoccupation(user_input: ChildEconOccupation):
    con = get_db()
    childeconoccupation = con.sql(f"""SELECT District,
                "{user_input.age_column}",
                occupations
                FROM econ_active_child_occupation
                WHERE sex = '{user_input.sex}'
                AND locality = '{user_input.locality}'
                AND education = '{user_input.education}'
                """).df()
    
    shp = get_shp(con)
    
    occupations = list(childeconoccupation['occupations'].unique())

    childeconoccupation = childeconoccupation.pivot(index='District', values=user_input.age_column, columns='occupations')
    
    childeconoccupation = childeconoccupation.div(childeconoccupation.sum(axis=1), axis=0) * 100

    childeconoccupation = childeconoccupation.round(2)

    childeconoccupation = childeconoccupation.reset_index()

    childeconoccupation = childeconoccupation.melt(id_vars='District', value_vars=occupations, value_name=user_input.age_column)
    
    childeconoccupation = childeconoccupation[childeconoccupation['occupations']==user_input.occupations][['District', user_input.age_column]]

    selected = shp.merge(childeconoccupation, on='District').merge(childeconoccupation, left_on='Region', right_on='District').drop(['District_y'], axis=1)

    selected = selected.rename(columns={'District_x':'District', f'{user_input.age_column}_x':user_input.age_column, f'{user_input.age_column}_y':'Regional_percentage'})

    selected['National_percentage'] = childeconoccupation[childeconoccupation['District']=='Ghana'][user_input.age_column].values[0]

    con.close()

    return selected.to_geo_dict() 
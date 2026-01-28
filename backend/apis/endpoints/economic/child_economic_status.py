from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from typing import List, Literal, Optional
from apis.data_store import get_db, get_shp

router_childeconstatus = APIRouter()

class ChildEconStatus(BaseModel):
    
    age_column:Literal["All ages",'5-9', '10-14']
        
    sex:Literal['Both Sexes', 'Male', 'Female']
        
    locality: Literal['All Locality Types','Rural', 'Urban']
        
    education: Literal['Total', 'Never attended', 'Nursery', 'Kindergarten', 'Primary','JSS/JHS', 'SSS/SHS', 'Secondary', 'Voc/technical/commercial']
        
    active_status: Literal["Not Economically Active", "Economically Active"]
    

@router_childeconstatus.post("/child_econ_status")
@cache(expire=60 * 5)
def get_childeconstatus(user_input: ChildEconStatus):

    con = get_db()
    childeconstatus = con.sql(f"""SELECT District,
                "{user_input.age_column}",
                active_status
                FROM children_economic_status
                WHERE sex = '{user_input.sex}'
                AND locality = '{user_input.locality}'
                AND education = '{user_input.education}'
                """).df()
    
    shp = get_shp(con)
    
    statuses = list(childeconstatus['active_status'].unique())

    childeconstatus = childeconstatus.pivot(index='District', values=user_input.age_column, columns='active_status')
    
    childeconstatus = childeconstatus.div(childeconstatus.sum(axis=1), axis=0) * 100

    childeconstatus = childeconstatus.round(2)

    childeconstatus = childeconstatus.reset_index()

    childeconstatus = childeconstatus.melt(id_vars='District', value_vars=statuses, value_name=user_input.age_column)
    
    childeconstatus = childeconstatus[childeconstatus['active_status']==user_input.active_status][['District', user_input.age_column]]

    selected = shp.merge(childeconstatus, on='District').merge(childeconstatus, left_on='Region', right_on='District').drop(['District_y'], axis=1)

    selected = selected.rename(columns={'District_x':'District', f'{user_input.age_column}_x':user_input.age_column, f'{user_input.age_column}_y':'Regional_percentage'})

    selected['National_percentage'] = childeconstatus[childeconstatus['District']=='Ghana'][user_input.age_column].values[0]

    con.close()

    return selected.to_geo_dict() 
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from typing import List, Literal, Optional
from apis.data_store import get_db, get_shp

router_childeconindustry = APIRouter()

class ChildEconIndustry(BaseModel):
    
    age_column:Literal["All ages",'5-9', '10-14']
        
    sex:Literal['Both Sexes', 'Male', 'Female']
        
    locality: Literal['All Locality Types','Rural', 'Urban']
        
    education: Literal['Total', 'Never attended', 'Nursery', 'Kindergarten', 'Primary','JSS/JHS', 'SSS/SHS', 'Secondary', 'Voc/technical/commercial']
        
    industry: Literal['Agriculture, forestry and fishing','Mining and quarrying', 'Manufacturing', 'Electricity, gas, steam and air conditioning supply',
                            'Water supply; sewerage, waste management and remediation activities','Construction','Wholesale and retail trade; repair of motor vehicles and motorcycles',
                            'Transportation and storage','Accommodation and food service activities','Arts, entertainment and recreation','Other service activities',
                            'Activities of households as employers; undifferentiated goods- and services-prod']
    

@router_childeconindustry.post("/child_econ_industry")
@cache(expire=60 * 5)
def get_childeconindustry(user_input: ChildEconIndustry):

    con = get_db()
    childeconindustry = con.sql(f"""SELECT District,
                "{user_input.age_column}",
                industry
                FROM economic_active_child_industry
                WHERE sex = '{user_input.sex}'
                AND locality = '{user_input.locality}'
                AND education = '{user_input.education}'
                """).df()
    
    shp = get_shp(con)
    
    industries = list(childeconindustry['industry'].unique())

    childeconindustry = childeconindustry.pivot(index='District', values=user_input.age_column, columns='industry')
    
    childeconindustry = childeconindustry.div(childeconindustry.sum(axis=1), axis=0) * 100

    childeconindustry = childeconindustry.round(2)

    childeconindustry = childeconindustry.reset_index()

    childeconindustry = childeconindustry.melt(id_vars='District', value_vars=industries, value_name=user_input.age_column)
    
    childeconindustry = childeconindustry[childeconindustry['industry']==user_input.industry][['District', user_input.age_column]]

    selected = shp.merge(childeconindustry, on='District').merge(childeconindustry, left_on='Region', right_on='District').drop(['District_y'], axis=1)

    selected = selected.rename(columns={'District_x':'District', f'{user_input.age_column}_x':user_input.age_column, f'{user_input.age_column}_y':'Regional_percentage'})

    selected['National_percentage'] = childeconindustry[childeconindustry['District']=='Ghana'][user_input.age_column].values[0]

    con.close()

    return selected.to_geo_dict() 
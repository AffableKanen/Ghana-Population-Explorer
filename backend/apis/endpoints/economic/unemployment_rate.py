from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from typing import List, Literal, Optional
from apis.data_store import get_db, get_shp

router_unemployment_rate = APIRouter() 

class Unemployment(BaseModel):
    
    age_column:Literal ["All ages","15-19","20-24","25-29","30-34","35-39","40-44","45-49","50-54","55-59","60-64","65-69","70-74","75-79","80-84","85-89","90-94"]
        
    sex:Literal['Both Sexes', 'Male', 'Female']
        
    locality: Literal['All Locality Types','Rural', 'Urban']
        
    education: Literal["Total","Never attended","Nursery","Kindergarten", "Primary","JSS/JHS","Middle", "SSS/SHS","Secondary","Voc/technical/commercial",
                       "Post middle/secondary Certificate","Post middle/secondary Diploma","Tertiary/HND","Tertiary - Bachelor's Degree","Tertiary - Post graduate Certificate/Diploma",
                       "Tertiary - Master's Degree","Tertiary - PhD", "Other (specify)"]

@router_unemployment_rate.post("/unemployment_rate")
@cache(expire=60 * 5)
def get_unemployment(user_input: Unemployment):
    # shp = DATA['districts_shapefile']
    # unemployment = DATA["unemployment_rate"]

    # unemployment = unemployment.loc[(unemployment['sex']==user_input.sex)&
    #                               (unemployment['locality']==user_input.locality)&
    #                               (unemployment['education']==user_input.education), 
    #                               ['District', user_input.age_column]]
    con = get_db()
    unemployment = con.sql(f"""SELECT District,
                "{user_input.age_column}"
                FROM unemployment_rate
                WHERE sex = '{user_input.sex}'
                AND locality = '{user_input.locality}'
                AND education = '{user_input.education}'
                """).df()
    
    shp = get_shp(con)

    unemployment[user_input.age_column] = unemployment[user_input.age_column].round(2)

    selected = shp.merge(unemployment, on='District').merge(unemployment, left_on='Region', right_on='District').drop(['District_y'], axis=1)

    selected = selected.rename(columns={'District_x':'District', f'{user_input.age_column}_x':user_input.age_column, f'{user_input.age_column}_y':'Regional_percentage'})

    selected['National_percentage'] = unemployment[unemployment['District']=='Ghana'][user_input.age_column].values[0]

    con.close()

    return selected.to_geo_dict() 
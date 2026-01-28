from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from typing import List, Literal, Optional
from apis.data_store import get_db, get_shp

router_econactiveindustry = APIRouter()

class EconActiveIndustry(BaseModel):
    
    age_column:Literal ["All ages","15-19","20-24","25-29","30-34","35-39","40-44","45-49","50-54","55-59","60-64","65-69","70-74","75-79","80-84","85-89","90-94"]
        
    sex:Literal['Both Sexes', 'Male', 'Female']
        
    locality: Literal['All Locality Types','Rural', 'Urban']
        
    education: Literal["Total","Never attended","Nursery","Kindergarten", "Primary","JSS/JHS","Middle", "SSS/SHS","Secondary","Voc/technical/commercial",
                       "Post middle/secondary Certificate","Post middle/secondary Diploma","Tertiary/HND","Tertiary - Bachelor's Degree","Tertiary - Post graduate Certificate/Diploma",
                       "Tertiary - Master's Degree","Tertiary - PhD", "Other (specify)"]
        
    industries: Literal["Agriculture, forestry and fishing","Manufacturing","Transportation and storage","Wholesale and retail trade; repair of motor vehicles and motorcycles",
                      "Other service activities","Accommodation and food service activities", "Construction","Arts, entertainment and recreation", "Education",
                      "Electricity, gas, steam and air conditioning supply","Water supply; sewerage, waste management and remediation activities",
                      "Public administration and defence; compulsory social security", "Activities of households as employers; undifferentiated goods- and services-prod",
                      "Mining and quarrying", "Professional, scientific and technical activities", "Human health and social work activities","Information and communication",
                      "Real estate activities","Financial and insurance activities","Administrative and support service activities", 
                      "Activities of extraterritorial organizations and bodies"]
    

@router_econactiveindustry.post("/econ_active_industry")
@cache(expire=60 * 5)
def get_econactiveindustry(user_input: EconActiveIndustry):
    
    con = get_db()
    econactiveindustry = con.sql(f"""SELECT District,
                "{user_input.age_column}",
                industries
                FROM economic_active_population_industry
                WHERE sex = '{user_input.sex}'
                AND locality = '{user_input.locality}'
                AND education = '{user_input.education}'
                """).df()
    
    shp = get_shp(con)
    
    industries = list(econactiveindustry['industries'].unique())

    econactiveindustry = econactiveindustry.pivot(index='District', values=user_input.age_column, columns='industries')
    
    econactiveindustry = econactiveindustry.div(econactiveindustry.sum(axis=1), axis=0) * 100

    econactiveindustry = econactiveindustry.round(2)

    econactiveindustry = econactiveindustry.reset_index()

    econactiveindustry = econactiveindustry.melt(id_vars='District', value_vars=industries, value_name=user_input.age_column)
    
    econactiveindustry = econactiveindustry[econactiveindustry['industries']==user_input.industries][['District', user_input.age_column]]

    selected = shp.merge(econactiveindustry, on='District').merge(econactiveindustry, left_on='Region', right_on='District').drop(['District_y'], axis=1)

    selected = selected.rename(columns={'District_x':'District', f'{user_input.age_column}_x':user_input.age_column, f'{user_input.age_column}_y':'Regional_percentage'})

    selected['National_percentage'] = econactiveindustry[econactiveindustry['District']=='Ghana'][user_input.age_column].values[0]

    con.close()

    return selected.to_geo_dict() 
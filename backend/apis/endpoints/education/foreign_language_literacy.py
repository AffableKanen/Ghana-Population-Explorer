from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from typing import List, Literal, Optional
from apis.data_store import get_db, get_shp

router_foreign_language_literacy = APIRouter()

class ForeignLanguageLiteracy(BaseModel):
    
    age_column:Literal['All ages', '6-11', '12-14', '15-19', '20-24', '25-29', '30-34','35-39', '40-44', '45-49', '50-54', '55-59', '60-64', 
                       '65-69', '70-74','75-79', '80-84', '85-89', '90-94', '95-99', '100+']
        
    sex:Literal['Both Sexes', 'Male', 'Female']
        
    locality: Literal['All Locality Types','Rural', 'Urban']
        
    education: Literal['Total', 'Never attended', 'Nursery', 'Kindergarten', 'Primary','JSS/JHS', 'Middle', 'SSS/SHS', 'Secondary',
                       'Voc/technical/commercial', 'Post middle/secondary Certificate','Post middle/secondary Diploma', 'Tertiary/HND',
                       "Tertiary - Bachelor's Degree",'Tertiary - Post graduate Certificate/Diploma',"Tertiary - Master's Degree", 'Tertiary - PhD', 'Other (specify)']
    
    language: Literal['Ghanaian_Language', 'English', 'French', 'Arabic', 'Russian','Hausa', 'Spanish','German', 'Hindi', 'Chinese','Swahili', 'Japanese','Other']
    
def get_df(con,age_col, sex, edu, locality):
    df = con.sql(f"""SELECT District,
        "{age_col}", language FROM foreign_language_literacy 
        WHERE sex = '{sex}'
        AND locality = '{locality}'
        AND education = '{edu}'
        """).df()
    return df

@router_foreign_language_literacy.post("/foreign_language_literacy")
@cache(expire=60 * 5)
def get_foreign_language_literacy(user_input: ForeignLanguageLiteracy):

    con = get_db()

    foreignlanguageliteracy = get_df(con, user_input.age_column, user_input.sex, user_input.education, user_input.locality)

    languages = list(foreignlanguageliteracy['language'].unique())

    foreignlanguageliteracy = foreignlanguageliteracy.pivot(index='District', values=user_input.age_column, columns='language')
    
    foreignlanguageliteracy = foreignlanguageliteracy.div(foreignlanguageliteracy.sum(axis=1), axis=0) * 100

    foreignlanguageliteracy = foreignlanguageliteracy.round(2)
    foreignlanguageliteracy = foreignlanguageliteracy.reset_index()

    foreignlanguageliteracy = foreignlanguageliteracy.melt(id_vars='District', value_vars=languages, value_name=user_input.age_column)
    
    foreignlanguageliteracy = foreignlanguageliteracy[foreignlanguageliteracy['language']==user_input.language][['District', user_input.age_column]]
    shp = get_shp(con)

    selected = shp.merge(foreignlanguageliteracy, on='District').merge(foreignlanguageliteracy, left_on='Region', right_on='District').drop(['District_y'], axis=1)
    selected = selected.rename(columns={'District_x':'District', f'{user_input.age_column}_x':user_input.age_column, f'{user_input.age_column}_y':'Regional_percentage'})

    selected['National_percentage'] = foreignlanguageliteracy[foreignlanguageliteracy['District']=='Ghana'][user_input.age_column].values[0]

    con.close()
    return selected.to_geo_dict() 
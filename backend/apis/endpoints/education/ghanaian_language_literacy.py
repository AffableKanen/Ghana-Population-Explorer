from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from typing import List, Literal, Optional
from apis.data_store import get_db, get_shp

router_ghanaian_language_literacy = APIRouter()

class GhanaianLanguageLiteracy(BaseModel):
    
    age_column:Literal['All ages', '6-11', '12-14', '15-19', '20-24', '25-29', '30-34','35-39', '40-44', '45-49', '50-54', '55-59', '60-64', 
                       '65-69', '70-74','75-79', '80-84', '85-89', '90-94', '95-99', '100+']
        
    sex:Literal['Both Sexes', 'Male', 'Female']
        
    locality: Literal['All Locality Types','Rural', 'Urban']
        
    education: Literal['Total', 'Never attended', 'Nursery', 'Kindergarten', 'Primary','JSS/JHS', 'Middle', 'SSS/SHS', 'Secondary',
                       'Voc/technical/commercial', 'Post middle/secondary Certificate','Post middle/secondary Diploma', 'Tertiary/HND',
                       "Tertiary - Bachelor's Degree",'Tertiary - Post graduate Certificate/Diploma',"Tertiary - Master's Degree", 'Tertiary - PhD', 'Other (specify)']
    
    language: Literal['Akwapim_Twi', 'Asante_Twi', 'Fante', 'Nzema', 'Ga', 'Dangme','Ewe', 'Dagbani', 'Gonja', 'Dagaari', 'Kasem', 'Gruni']
    
def get_df(con,age_col, sex, edu, locality):
    df = con.sql(f"""SELECT District,
        "{age_col}", language FROM gh_language_literacy 
        WHERE sex = '{sex}'
        AND locality = '{locality}'
        AND education = '{edu}'
        """).df()
    return df

@router_ghanaian_language_literacy.post("/ghanaian_language_literacy")
@cache(expire=60 * 5)
def get_ghanaian_language_literacy(user_input: GhanaianLanguageLiteracy):

    con = get_db()

    ghanaianlanguageliteracy = get_df(con, user_input.age_column, user_input.sex, user_input.education, user_input.locality)

    languages = list(ghanaianlanguageliteracy['language'].unique())

    ghanaianlanguageliteracy = ghanaianlanguageliteracy.pivot(index='District', values=user_input.age_column, columns='language')
    
    ghanaianlanguageliteracy = ghanaianlanguageliteracy.div(ghanaianlanguageliteracy.sum(axis=1), axis=0) * 100

    ghanaianlanguageliteracy = ghanaianlanguageliteracy.round(2)
    ghanaianlanguageliteracy = ghanaianlanguageliteracy.reset_index()

    ghanaianlanguageliteracy = ghanaianlanguageliteracy.melt(id_vars='District', value_vars=languages, value_name=user_input.age_column)
    
    ghanaianlanguageliteracy = ghanaianlanguageliteracy[ghanaianlanguageliteracy['language']==user_input.language][['District', user_input.age_column]]
    shp = get_shp(con)

    selected = shp.merge(ghanaianlanguageliteracy, on='District').merge(ghanaianlanguageliteracy, left_on='Region', right_on='District').drop(['District_y'], axis=1)
    selected = selected.rename(columns={'District_x':'District', f'{user_input.age_column}_x':user_input.age_column, f'{user_input.age_column}_y':'Regional_percentage'})

    selected['National_percentage'] = ghanaianlanguageliteracy[ghanaianlanguageliteracy['District']=='Ghana'][user_input.age_column].values[0]

    con.close()
    return selected.to_geo_dict() 
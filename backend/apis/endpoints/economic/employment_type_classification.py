from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from typing import List, Literal, Optional
from apis.data_store import get_db, get_shp

router_employment_classification = APIRouter() 

class EmploymentClassification(BaseModel):
    
    age_column:Literal ["All ages","15-19","20-24","25-29","30-34","35-39","40-44","45-49","50-54","55-59","60-64","65-69","70-74","75-79","80-84","85-89","90-94"]
        
    sex:Literal['Both Sexes', 'Male', 'Female']
        
    locality: Literal['All Locality Types','Rural', 'urban']
        
    education: Literal["Total","Never attended","Nursery","Kindergarten", "Primary","JSS/JHS","Middle", "SSS/SHS","Secondary","Voc/technical/commercial",
                       "Post middle/secondary Certificate","Post middle/secondary Diploma","Tertiary/HND","Tertiary - Bachelor's Degree","Tertiary - Post graduate Certificate/Diploma",
                       "Tertiary - Master's Degree","Tertiary - PhD", "Other (specify)"]
        
    status: Literal['Employee', 'Self-employed without employees', 'Self-employed with employees', 'Casual worker', 'Contributing family worker', 
                    'Paid apprentice', 'Unpaid apprentice', 'Domestic worker', 'Other']

@router_employment_classification.post("/employment_type_classification")
@cache(expire=60 * 5)
def get_employmentclassification(user_input: EmploymentClassification):

    con = get_db()
    employmentclassification = con.sql(f"""SELECT District,
                "{user_input.age_column}",
                status
                FROM employmnet_classification
                WHERE sex = '{user_input.sex}'
                AND locality = '{user_input.locality}'
                AND education = '{user_input.education}'
                """).df()
    
    shp = get_shp(con)
    
    statuses = list(employmentclassification['status'].unique())

    employmentclassification = employmentclassification.pivot(index='District', values=user_input.age_column, columns='status')
    
    employmentclassification = employmentclassification.div(employmentclassification.sum(axis=1), axis=0) * 100

    employmentclassification = employmentclassification.round(2)

    employmentclassification = employmentclassification.reset_index()

    employmentclassification = employmentclassification.melt(id_vars='District', value_vars=statuses, value_name=user_input.age_column)
    
    employmentclassification = employmentclassification[employmentclassification['status']==user_input.status][['District', user_input.age_column]]

    selected = shp.merge(employmentclassification, on='District').merge(employmentclassification, left_on='Region', right_on='District').drop(['District_y'], axis=1)

    selected = selected.rename(columns={'District_x':'District', f'{user_input.age_column}_x':user_input.age_column, f'{user_input.age_column}_y':'Regional_percentage'})

    selected['National_percentage'] = employmentclassification[employmentclassification['District']=='Ghana'][user_input.age_column].values[0]

    con.close()

    return selected.to_geo_dict() 
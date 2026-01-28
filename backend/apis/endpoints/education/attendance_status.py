from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from typing import List, Literal, Optional
from apis.data_store import get_db, get_shp

router_attendance_status = APIRouter()

class AttendanceStatus(BaseModel):
    
    age_column:Literal['All ages', '3-5', '6-10', '11-14', '15-19', '20-24', '25-29', '30-34','35-39', '40-44', '45-49', '50-54', '55-59', '60-64', 
                       '65-69', '70-74','75-79', '80-84', '85-89', '90-94', '95-99', '100+']
        
    sex:Literal['Both Sexes', 'Male', 'Female']
        
    locality: Literal['All Locality Types','Rural', 'Urban']
    
    attendance_status: Literal['Attended in the past', 'Attending now', 'Never attended']
    
def get_df(con,age_col, sex, locality): 
    df = con.sql(f"""SELECT District,
        "{age_col}", attendace_status FROM attendance_status 
        WHERE sex = '{sex}'
        AND locality = '{locality}'
        """).df()
    return df

@router_attendance_status.post("/attendance_status")
@cache(expire=60 * 5)
def get_attendance_status(user_input: AttendanceStatus): 

    con = get_db()

    attendancestatus = get_df(con, user_input.age_column, user_input.sex, user_input.locality)

    status = list(attendancestatus['attendace_status'].unique())

    attendancestatus = attendancestatus.pivot(index='District', values=user_input.age_column, columns='attendace_status')
    
    attendancestatus = attendancestatus.div(attendancestatus.sum(axis=1), axis=0) * 100
    attendancestatus = attendancestatus.round(2)
    attendancestatus = attendancestatus.reset_index()
    attendancestatus = attendancestatus.melt(id_vars='District', value_vars=status, value_name=user_input.age_column)
    
    attendancestatus = attendancestatus[attendancestatus['attendace_status']==user_input.attendance_status][['District', user_input.age_column]]
    shp = get_shp(con)

    selected = shp.merge(attendancestatus, on='District').merge(attendancestatus, left_on='Region', right_on='District').drop(['District_y'], axis=1)
    selected = selected.rename(columns={'District_x':'District', f'{user_input.age_column}_x':user_input.age_column, f'{user_input.age_column}_y':'Regional_percentage'})

    selected['National_percentage'] = attendancestatus[attendancestatus['District']=='Ghana'][user_input.age_column].values[0]

    con.close()
    return selected.to_geo_dict() 
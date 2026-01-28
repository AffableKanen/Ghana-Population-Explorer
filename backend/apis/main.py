from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as redis
from apis.endpoints.disability import total_status
from apis.endpoints.disability import seeing
from apis.endpoints.disability import hearing
from apis.endpoints.disability import remembering
from apis.endpoints.disability import physical
from apis.endpoints.disability import selfcare
from apis.endpoints.disability import speech
from apis.endpoints.economic import child_economic_status
from apis.endpoints.economic import child_econact_industry
from apis.endpoints.economic import econ_active_pop_status
from apis.endpoints.economic import econ_active_pop_industry
from apis.endpoints.economic import econ_active_child_occup
from apis.endpoints.economic import econ_active_pop_occupation
from apis.endpoints.economic import sector_employment
from apis.endpoints.economic import employment_type_classification
from apis.endpoints.economic import unemployment_rate
from apis.endpoints.education import past_attendance
from apis.endpoints.education import current_in_school
from apis.endpoints.education import literacy_status
from apis.endpoints.education import foreign_language_literacy
from apis.endpoints.education import ghanaian_language_literacy
from apis.endpoints.education import educational_attainment
from apis.endpoints.education import literacy_language_count
from apis.endpoints.education import attendance_status


app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React runs here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

@app.on_event("startup")
async def startup_event():
    redis_client = redis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")

app.include_router(total_status.router) 
app.include_router(seeing.router_seeing)  
app.include_router(hearing.router_hearing)  
app.include_router(remembering.router_remembering)
app.include_router(physical.router_physical)
app.include_router(selfcare.router_selfcare)
app.include_router(speech.router_speech)
app.include_router(child_economic_status.router_childeconstatus)
app.include_router(child_econact_industry.router_childeconindustry)
app.include_router(econ_active_pop_status.router_econactivestatus)
app.include_router(econ_active_pop_industry.router_econactiveindustry)
app.include_router(econ_active_child_occup.router_childeconoccupation)
app.include_router(econ_active_pop_occupation.router_econactiveoccupation)
app.include_router(sector_employment.router_sectoremployment)
app.include_router(employment_type_classification.router_employment_classification)
app.include_router(unemployment_rate.router_unemployment_rate)
app.include_router(past_attendance.router_past_attendance)
app.include_router(current_in_school.router_current_attendance)
app.include_router(literacy_status.router_literacy_status)
app.include_router(foreign_language_literacy.router_foreign_language_literacy)
app.include_router(ghanaian_language_literacy.router_ghanaian_language_literacy)
app.include_router(educational_attainment.router_educational_attainment)
app.include_router(literacy_language_count.router_literacy_language_count)
app.include_router(attendance_status.router_attendance_status)
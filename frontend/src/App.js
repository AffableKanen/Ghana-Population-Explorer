import React, { act } from 'react';
import logo from './logo.svg';
import { useState, useEffect } from 'react';
import './App.css';
import Upper from './upper';
import Disability from './components/disability/disability';
import EconomicActivity from './components/economic/economic';
import Education from './components/education/education';
import Fertility from './components/fertility/fertility';
import Housing from './components/housing/housing';
import Ict from './components/ict/ict';
import Hdi from './components/hdi/hdi';
import Poverty from './components/poverty/poverty';
import Population from './components/population/population';
import Structures from './components/structures/structures';
import Water from './components/water/water';
import Categories from './categories';
import TotalStatusMap from './components/disability/maps/total_status_map';
import SeeingMap from './components/disability/maps/seeing_map';
import HearingMap from './components/disability/maps/hearing_map';
import RememberingMap from './components/disability/maps/remembering_map';
import PhysicalMap from './components/disability/maps/physical_map';
import SelfcareMap from './components/disability/maps/selfcare_map';
import SpeechMap from './components/disability/maps/speech_map';
import ChildEconStatusMap from './components/economic/maps/child_econ_status_map';
import ChildEconIndustryMap from './components/economic/maps/child_econ_industry_map';
import EconActiveStatusMap from './components/economic/maps/econ_active_status_map';
import EconActiveIndustrysMap from './components/economic/maps/econ_active_industry_map';
import ChildEconOccupationMap from './components/economic/maps/child_econ_occupation_map';
import EconActiveOccupationMap from './components/economic/maps/econ_active_population_map_occupation';
import SectorEmploymentMap from './components/economic/maps/sector_employment_map';
import EmploymentTypeClassificationMap from './components/economic/maps/employment_type_classification_map';
import UnemploymentRateMap from './components/economic/maps/unemployment_rate_map';
import PastAttendanceMap from './components/education/maps/past_attendance_map';
import CurrentAttendanceMap from './components/education/maps/current_attendance_map';
import LiteracyStatusMap from './components/education/maps/literacy_status_map';
import ForeignLanguageLiteracyMap from './components/education/maps/foreign_language_literacy_map';
import GhanaianLanguageLiteracyMap from './components/education/maps/ghanaian_language_literacy_map';
import EducationalAttainmentMap from './components/education/maps/educational_attainment_map';
import LiteracyLanguageCountMap from './components/education/maps/literacy_language_count_map';
import AttendanceStatusMap from './components/education/maps/attendance_status_map';


function App() {

  const [activeCategory, setActiveCategory] = useState("DISABILITY");
  
  const [activeSubCategory, setActiveSubCategory] = useState(

  activeCategory === "DISABILITY"
    ? "Difficulty Status"
    : activeCategory === "ECONOMIC ACTIVITY"
    ? "Economic Activity (5-14 years)"
    : activeCategory === "EDUCATION & LITERACY"
    ? "Attended School in the Past"
    : activeCategory === "FERTILITY & MORTALITY"
    ? "Children Ever Born"
    :activeCategory === "HOUSING"
    ? "Bath Facilities"
    :activeCategory === "ICT"
    ? "Smartphone Ownership"
    :activeCategory === "HUMAN DEVELOPMENT INDICATORS"
    ? "Gender Development Index Indicators"
    :activeCategory === "MULTIDIMENSIONAL POVERTY"
    ? "Multidimensional Poverty Metrics by Education"
    :activeCategory === "POPULATION"
    ? "Average Household Size"
    :activeCategory === "STRUCTURES"
    ? "Level of Completion of Residential Structures"
    :activeCategory === "WATER & SANITATION"
    ? "Point of Defecation (Households without Toilet)"
    : ""
);


  function handleCategoryClick(category) {
    setActiveCategory(category);
    // setActiveSubCategory(""); // reset subcategory when category changes
  }

  function handleSubCategoryClick(subcategory) {
    setActiveSubCategory(subcategory);
      
  }

  return (
    <div className="App" style={{ backgroundColor: "#E6E6FA", marginLeft: "50px", marginRight: "50px" }}>
      <Upper />
      <Categories
        handleCategoryClick={handleCategoryClick}
        activeCategory={activeCategory}
      />

      {activeCategory === "DISABILITY" && <Disability handleSubCategoryClick={handleSubCategoryClick} activeSubCategory={activeSubCategory}/>}
      {activeCategory === "ECONOMIC ACTIVITY" && <EconomicActivity handleSubCategoryClick={handleSubCategoryClick} activeSubCategory={activeSubCategory}/>}
      {activeCategory === "EDUCATION & LITERACY" && <Education handleSubCategoryClick={handleSubCategoryClick} activeSubCategory={activeSubCategory}/>}
      {activeCategory === "FERTILITY & MORTALITY" && <Fertility handleSubCategoryClick={handleSubCategoryClick} activeSubCategory={activeSubCategory}/>}
      {activeCategory === "HOUSING" && <Housing handleSubCategoryClick={handleSubCategoryClick} activeSubCategory={activeSubCategory}/>}
      {activeCategory === "ICT" && <Ict handleSubCategoryClick={handleSubCategoryClick} activeSubCategory={activeSubCategory}/>}
      {activeCategory === "HUMAN DEVELOPMENT INDICATORS" && <Hdi handleSubCategoryClick={handleSubCategoryClick} activeSubCategory={activeSubCategory}/>}
      {activeCategory === "MULTIDIMENSIONAL POVERTY" && <Poverty handleSubCategoryClick={handleSubCategoryClick} activeSubCategory={activeSubCategory}/>}
      {activeCategory === "POPULATION" && <Population handleSubCategoryClick={handleSubCategoryClick} activeSubCategory={activeSubCategory}/>}
      {activeCategory === "STRUCTURES" && <Structures handleSubCategoryClick={handleSubCategoryClick} activeSubCategory={activeSubCategory}/>}
      {activeCategory === "WATER & SANITATION" && <Water handleSubCategoryClick={handleSubCategoryClick} activeSubCategory={activeSubCategory}/>}
      
      {/* Disability Subcategories */}
      {activeSubCategory === "Difficulty Status" && <TotalStatusMap/>}
      {activeSubCategory === "Difficulty in Seeing" && <SeeingMap/>}
      {activeSubCategory === "Difficulty in Hearing" && <HearingMap/>}
      {activeSubCategory === "Difficulty in Remembering/Concentration" && <RememberingMap/>}
      {activeSubCategory === "Physical Disability" && <PhysicalMap/>}
      {activeSubCategory === "Difficulty in Self-care" && <SelfcareMap/>}
      {activeSubCategory === "Difficulty in Speech" && <SpeechMap/>}

      {/* Economic Activity Subcategories */}
      {activeSubCategory === "Economic Activity (5-14 years)" && <ChildEconStatusMap/>}
      {activeSubCategory === "Economic Activity by Industry (5-14 years old)" && <ChildEconIndustryMap/>}
      {activeSubCategory === "Economic Activity (15+)" && <EconActiveStatusMap/>}
      {activeSubCategory === "Employment by Industry" && <EconActiveIndustrysMap/>}
      {activeSubCategory === "Economic Activity by Occupation (5-14 years)" && <ChildEconOccupationMap/>}
      {activeSubCategory === "Employment by Occupation" && <EconActiveOccupationMap/>}
      {activeSubCategory === "Employment by Sector" && <SectorEmploymentMap/>}
      {activeSubCategory === "Employment Status" && <EmploymentTypeClassificationMap/>}
      {activeSubCategory === "Unemployment Rate" && <UnemploymentRateMap/>}

      {/* Education Subcategories */}
      {activeSubCategory === "Attended School in the Past" && <PastAttendanceMap/>}
      {activeSubCategory === "Currently in School" && <CurrentAttendanceMap/>}
      {activeSubCategory === "Literacy Status" && <LiteracyStatusMap/>}
      {activeSubCategory === "Foreign Language Literacy" && <ForeignLanguageLiteracyMap/>}
      {activeSubCategory === "Ghanaian Language Literacy" && <GhanaianLanguageLiteracyMap/>}
      {activeSubCategory === "Educational Attainment" && <EducationalAttainmentMap/>}
      {activeSubCategory === "Number of Languages Spoken" && <LiteracyLanguageCountMap/>}
      {activeSubCategory === "School Attendance Status" && <AttendanceStatusMap/>}

      {/* <div style={{ marginTop: "20px", marginBottom: "20px", fontSize: "12px" }}>
        Data Source: Ghana Statistical Service (GSS) - 2021 Population and Housing Census (PHC) & 2021 Ghana Disability Report | Developed by Zurikanen Iddrisu
      </div> */}
      
    </div>
  );
}
export default App;
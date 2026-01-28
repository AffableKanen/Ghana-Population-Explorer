import React from "react";

function Education({ handleSubCategoryClick, activeSubCategory }) {
    const subcategories = [
        "Attended School in the Past",
        "Currently in School",
        "Foreign Language Literacy",   
        "Educational Attainment",
        "Ghanaian Language Literacy",
        "Number of Languages Spoken",
        "Literacy Status",
        "School Attendance Status"]
    return (
        <div className="Education text-start">
            {subcategories.map((subcategory) => (
                <button key={subcategory} type="button" class="btn btn-primary btn-sm m-3" 
                    style={{
                    padding: "6px 4px",
                    backgroundColor:
                    activeSubCategory === subcategory ? "#5D3FD3" : "#AA336A",
                    color: "white",
                }}
          onClick={() => handleSubCategoryClick(subcategory)}>{subcategory}</button>
            ))}
            
            <hr/>
        </div>
    );
}

export default Education;
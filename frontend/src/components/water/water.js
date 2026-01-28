import React from "react";

function Water({ handleSubCategoryClick, activeSubCategory }) {
    const subcategories = [
        "Point of Defecation (Households without Toilet)",
        "Source of Water for Domestic Use",
        "Usage of Toilet Facility",
        "Source of Drinking Water",
        "Use of Improved Water Sources and Basic Drinking Water Services",
        "Solid Waste Disposal Method",
        "Solid Waste Storage",
        "Time Spent to Drinking Water Source",
        "Toilet Facility",
        "Levels of Toilet Service",
        "Type of Drophole",
        "Waste Water Disposal Method"
    ];
    return (
        <div className="Water text-start m-1">
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

export default Water;
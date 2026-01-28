import React from "react";

function Housing({ handleSubCategoryClick, activeSubCategory }) {
    const subcategories = [
        "Bath Facilities",
        "Cooking Fuel",
        "Cooking Space",
        "Dwelling Floor Construction Material",
        "Source of Lighting",
        "Number of Rooms",
        "Ownership Structure",
        "Number of Sleeping Rooms",
        "Tenure/Holding Arrangement",
        "Type of Dwelling",
        "Type of Residence",
        "Dwelling Roof Construction Material",
        "Dwelling Outer Wall Construction Material",]
    return (
        <div className="Housing text-start">
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

export default Housing;
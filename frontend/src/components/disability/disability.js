import React from "react";

function Disability({handleSubCategoryClick, activeSubCategory}) {
    const subcategories = [
        "Difficulty Status",
        "Difficulty in Seeing",
        "Difficulty in Hearing",
        "Difficulty in Remembering/Concentration",
        "Physical Disability",
        "Difficulty in Self-care",
        "Difficulty in Speech"]
    return (
        <div className="Disability text-start">
            {subcategories.map((subcategory) => (
                <button key={subcategory} type="button" class="btn btn-primary btn-sm m-3"
                style={{
                    padding: "2px 2px",
                    backgroundColor:
                    activeSubCategory === subcategory ? "#5D3FD3" : "#AA336A",
                    color: "white",}}
                    onClick={() => handleSubCategoryClick(subcategory)}
                >{subcategory}</button>
            ))}

            <hr/>
        </div>
    );
}

export default Disability;
import React from "react";

function Population({ handleSubCategoryClick, activeSubCategory }) {
    const subcategories = [
        "Average Household Size",
        "Place of Birth",
        "Major",
        "Health Coverage Status",
        "Household Size",
        "Nationality",
        "Total Population",
        "Population Projections",
        "Religious Affilliation"
    ];
    return (
        <div className="Population text-start">
            {subcategories.map((subcategory) => (
                <button
                    key={subcategory}
                    type="button"
                    className="btn btn-sm m-2"
                    style={{
                        padding: "6px 4px",
                        backgroundColor:
                            activeSubCategory === subcategory ? "#5D3FD3" : "#AA336A",
                        color: "white",
                    }}
                    onClick={() => handleSubCategoryClick(subcategory)}
                >
                    {subcategory}
                </button>
            ))}
            <hr />
        </div>
    );
}

export default Population;
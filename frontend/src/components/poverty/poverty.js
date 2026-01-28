import React from "react";

function Poverty({ handleSubCategoryClick, activeSubCategory }) {
    const subcategories = [
        "Multidimensional Poverty Metrics by Education",
        "Multidimensional Poverty Metrics by Industry",
        "Multidimensional Poverty Metrics by Locality",
        "Multidimensional Poverty Metrics",
        "Contributors to Multidimensional Poverty", 
    ];
    return (
        <div className="Poverty text-start">
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

export default Poverty;
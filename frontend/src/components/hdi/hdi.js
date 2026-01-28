import React from "react";

function Hdi({ handleSubCategoryClick, activeSubCategory }) {
    const subcategories = [
        "Gender Development Index Indicators",
        "Trends in Human Development Indicators"
    ];
    return (
        <div className="Hdi text-start">
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

export default Hdi;
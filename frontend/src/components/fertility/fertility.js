import React from "react";

function Fertility({ handleSubCategoryClick, activeSubCategory }) {
    const subcategories = [
        "Children Ever Born",
        "Children Ever Born (12 to 19 years)",
        "Surviving Children",
        "Mean Age at First Birth",
        "Mean Number of Children Ever Born",
        "Mean Number of Surviving Children",
        "Children Born in Last 12 Months",
        "Surviving Children Born in Last 12 Months"
    ];
    return (
        <div className="Fertility text-start">
            {subcategories.map((subcategory) => (
                <button
                    key={subcategory}
                    type="button"
                    class="btn btn-primary btn-sm m-3"
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
            <hr/>
        </div>
    );
}

export default Fertility;
import React from "react";

function Structures({ handleSubCategoryClick, activeSubCategory }) {
    const subcategories = [
        "Level of Completion of Residential Structures",
        "Level of Completion of Structures",
        "Residential Structures",
        "Type of Structures"
    ];
    return (
        <div className="Structures text-start">
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

export default Structures;
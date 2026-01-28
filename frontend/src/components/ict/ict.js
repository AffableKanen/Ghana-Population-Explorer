import React from "react";

function Ict({ handleSubCategoryClick, activeSubCategory }) {
    const subcategories = [
        "Smartphone Ownership",
        "Non-Smartphone Ownership",
        "Tablet Ownership",
        "Laptop Ownership",
        "Mobile Phone Ownership",
        "Internet Usage",
        "Internet Usage on Tablet",
        "Internet Usage on Laptop Computer",
        "Internet Usage on Desktop Computer",
        "Internet Usage on Digital TV",
        "Internet Usage on Other Digital Device",
        "No Internet Usage on Any Device",
        "Usage of Smartphone",
        "Usage of Non-Smartphone",
        "Usage of Cordless Phone",
        "Usage of Tablet",
        "Usage of Laptop Computer",
        "Usage of Desktop Computer",
        "Usage of Radio Set",
        "Usage of Any IT Device",
        "Usage of Mobile Phone For Financial Transaction"
    ];
    return (
        <div className="Ict text-start">
            {subcategories.map((subcategory) => (
                <button
                    key={subcategory}
                    type="button"
                    class="btn btn-primary btn-sm m-3"
                    style={{
                        // padding: "6px 4px",
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

export default Ict;
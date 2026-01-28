import React from "react";

function EconomicActivity({ handleSubCategoryClick, activeSubCategory }) {
  const subcategories = [
    "Economic Activity (5-14 years)",
    "Economic Activity by Industry (5-14 years old)",
    "Economic Activity (15+)",
    "Employment by Industry",
    "Economic Activity by Occupation (5-14 years)",
    "Employment by Occupation",
    "Employment by Sector",
    "Employment Status",
    "Unemployment Rate",
  ];

  return (
    <div className="Economic text-start">
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

export default EconomicActivity;

import React from "react";

// create a function to to create buttons of all the categories
function Categories({ handleCategoryClick, activeCategory }) {
    const categories = [
      "DISABILITY",
      "ECONOMIC ACTIVITY",
      "EDUCATION & LITERACY",
      "FERTILITY & MORTALITY",
      "HOUSING",
      "HUMAN DEVELOPMENT INDICATORS",
      "ICT",
      "MULTIDIMENSIONAL POVERTY",
      "POPULATION",
      "STRUCTURES",
      "WATER & SANITATION",
    ];

    return (
      <div
        className="Categories text-start m-1"
      >
        {categories.map((category) => (
          <button
            key={category}
            type="button"
            className="btn btn-md m-1"
            style={{
              padding: "2px 2px",
              backgroundColor:
                activeCategory === category ? "#ff9800" : "#DA70D6",
              color: "white",
            }}
            onClick={() => handleCategoryClick(category)}
          >
            <b>{category}</b>
          </button>
        ))}
        <hr/>
      </div>
    );
  }

export default Categories;
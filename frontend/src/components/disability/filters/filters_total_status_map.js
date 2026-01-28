import React, { useState } from "react";

export default function Filters({ filters, setFilters }) {
  return (
    <div className="filters">
        <h4 className="text-center" style={{ color: "#fff", backgroundColor: "#702A2F", padding: "10px", borderRadius: "5px" }}> Filter by: </h4>
      {/* Age Column */}
      <div style={{ border: "2px solid #800020", padding: "8px", marginBottom: "6px", maxHeight: "190px", overflowY: "auto", backgroundColor: "#b33655ff" }}>
        <label className="fw-bold text-decoration-underline" style={{ color: "white" }}>AGE GROUP</label>
        {[
          { value: "All_ages", label: "All Ages" },
          { value: "age_5_9", label: "5-9" },
          { value: "age_10_14", label: "10-14" },
          { value: "age_15_17", label: "15-17" },
          { value: "age_18_19", label: "18-19" },
          { value: "age_20_24", label: "20-24" },
          { value: "age_25_29", label: "25-29" },
          { value: "age_30_34", label: "30-34" },
          { value: "age_35_39", label: "35-39" },
          { value: "age_40_44", label: "40-44" },
          { value: "age_45_49", label: "45-49" },
          { value: "age_50_54", label: "50-54" },
          { value: "age_55_59", label: "55-59" },
          { value: "age_60_64", label: "60-64" },
          { value: "age_65_69", label: "65-69" },
          { value: "age_70_74", label: "70-74" },
          { value: "age_75_79", label: "75-79" },
          { value: "age_80_84", label: "80-84" },
          { value: "age_85_89", label: "85-89" },
          { value: "age_90_94", label: "90-94" },
          { value: "age_95_99", label: "95-99" },
          { value: "age_100_plus", label: "100+" },
        ].map((opt) => (
          <div className="form-check" key={opt.value}>
            <input
              className="form-check-input"
              type="radio"
              name="age_column"
              value={opt.value}
              id={`age-${opt.value}`}
              checked={filters.age_column === opt.value}
              onChange={(e) =>
                setFilters({ ...filters, age_column: e.target.value })
              }
            />
            <label className="form-check-label" htmlFor={`age-${opt.value}`} style={{ color: "white" }}>
              {opt.label}
            </label>
          </div>
        ))}
      </div>

      {/* Sex */}
      <div style={{ border: "2px solid #800020", padding: "8px", marginBottom: "6px", backgroundColor: "#b33655ff" }}>
        <label className="fw-bold text-decoration-underline" style={{ color: "white" }}>SEX</label>
        {["Both Sexes", "Male", "Female"].map((opt) => (
          <div className="form-check" key={opt}>
            <input
              className="form-check-input"
              type="radio"
              name="sex"
              id={`sex-${opt}`}
              value={opt}
              checked={filters.sex === opt}
              onChange={(e) => setFilters({ ...filters, sex: e.target.value })}
            />
            <label className="form-check-label" htmlFor={`sex-${opt}`} style={{ color: "white" }}>
              {opt}
            </label>
          </div>
        ))}
      </div>

      {/* Locality */}
      <div style={{ border: "2px solid #c42f54ff", padding: "8px", marginBottom: "6px", backgroundColor: "#b33655ff"}}>
        <label className="fw-bold text-decoration-underline" style={{ color: "white" }}>LOCALITY</label>
        {["All Locality Types", "Rural", "Urban"].map((opt) => (
          <div className="form-check" key={opt}>
            <input
              className="form-check-input"
              type="radio"
              name="locality"
              id={`locality-${opt}`}
              value={opt}
              checked={filters.locality === opt}
              onChange={(e) =>
                setFilters({ ...filters, locality: e.target.value })
              }
            />
            <label className="form-check-label" htmlFor={`locality-${opt}`} style={{ color: "white" }}>
              {opt}
            </label>
          </div>
        ))}
      </div>

      {/* Education */}
      <div style={{ border: "2px solid #800020", padding: "8px", marginBottom: "6px", maxHeight: "180px", overflowY: "auto", backgroundColor: "#b33655ff" }}>
        <label className="fw-bold text-decoration-underline" style={{ color: "white" }}>EDUCATION</label>
        {[
          "Total",
          "Never attended",
          "Nursery",
          "Kindergarten",
          "Primary",
          "JSS/JHS",
          "Middle",
          "SSS/SHS",
          "Secondary",
          "Voc/technical/commercial",
          "Post middle/secondary Certificate",
          "Post middle/secondary Diploma",
          "Tertiary/HND",
          "Tertiary - Bachelor's Degree",
          "Tertiary - Post graduate Certificate/Diploma",
          "Tertiary - Master's Degree",
          "Tertiary - PhD",
          "Other (specify)",
        ].map((opt) => (
          <div className="form-check" key={opt}>
            <input
              className="form-check-input"
              type="radio"
              name="education"
              id={`edu-${opt}`}
              value={opt}
              checked={filters.education === opt}
              onChange={(e) =>
                setFilters({ ...filters, education: e.target.value })
              }
            />
            <label className="form-check-label" htmlFor={`edu-${opt}`} style={{ color: "white" }}>
              {opt}
            </label>
          </div>
        ))}
      </div>

    </div>
  );
}

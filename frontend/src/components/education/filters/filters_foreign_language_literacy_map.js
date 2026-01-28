import React, { useState } from "react";

export default function ForeignLanguageLiteracyFilters({ filters, setFilters }) {
  return (
    <div className="filters">
        <h4 className="text-center" style={{ color: "#fff", backgroundColor: "#702A2F", padding: "10px", borderRadius: "5px" }}> Filter by: </h4>
      {/* Age Column */}
      <div style={{ border: "2px solid #800020", padding: "8px", marginBottom: "6px", maxHeight: "120px", overflowY: "auto", backgroundColor: "#b33655ff" }}>
        <label className="fw-bold text-decoration-underline" style={{ color: "white" }}>AGE GROUP</label>
        {[
          { value: "All ages", label: "All Ages" },
          { value: "6-11", label: "6-11" },
          { value: "12-14", label: "12-14" },
          { value: "15-19", label: "15-19" },
          { value: "20-24", label: "20-24" },
          { value: "25-29", label: "25-29" },
          { value: "30-34", label: "30-34" },
          { value: "35-39", label: "35-39" },
          { value: "40-44", label: "40-44" },
          { value: "45-49", label: "45-49" },
          { value: "50-54", label: "50-54" },
          { value: "55-59", label: "55-59" },
          { value: "60-64", label: "60-64" },
          { value: "65-69", label: "65-69" },
          { value: "70-74", label: "70-74" },
          { value: "75-79", label: "75-79" },
          { value: "80-84", label: "80-84" },
          { value: "85-89", label: "85-89" },
          { value: "90-94", label: "90-94" },
          { value: "95-99", label: "95-99" },
          { value: "100+", label: "100+" },
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
      <div style={{ border: "2px solid #800020", padding: "8px", marginBottom: "6px", maxHeight: "110px", overflowY: "auto", backgroundColor: "#b33655ff" }}>
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
      <div style={{ border: "2px solid #c42f54ff", padding: "8px", marginBottom: "6px", maxHeight: "110px", overflowY: "auto", backgroundColor: "#b33655ff"}}>
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
      <div style={{ border: "2px solid #800020", padding: "8px", marginBottom: "6px", maxHeight: "140px", overflowY: "auto", backgroundColor: "#b33655ff" }}>
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
          "Other (specify)"
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

    {/* languages */}
      <div style={{ border: "2px solid #c42f54ff", padding: "8px", marginBottom: "6px", maxHeight: "120px", overflowY: "auto", backgroundColor: "#b33655ff"}}>
        <label className="fw-bold text-decoration-underline" style={{ color: "white" }}>LANGUAGE OF LITERACY</label>
        {['Ghanaian_Language', 'English', 'French', 'Arabic', 'Russian','Hausa', 'Spanish','German', 'Hindi', 'Chinese','Swahili', 'Japanese','Other'].map((opt) => (
          <div className="form-check" key={opt}>
            <input
              className="form-check-input"
              type="radio"
              name="language"
              id={`language-${opt}`}
              value={opt}
              checked={filters.language === opt}
              onChange={(e) =>
                setFilters({ ...filters, language: e.target.value })
              }
            />
            <label className="form-check-label" htmlFor={`language-${opt}`} style={{ color: "white" }}>
              {opt}
            </label>
          </div>
        ))}
      </div>                         

    </div>
  );
}

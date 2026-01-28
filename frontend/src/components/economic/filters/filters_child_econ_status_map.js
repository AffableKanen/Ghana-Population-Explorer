import React from "react";

export default function ChildEconStatusFilters({ filters, setFilters }) {
  return (
    <div className="filters">
        <h4 className="text-center" style={{ color: "#fff", backgroundColor: "#702A2F", padding: "10px", borderRadius: "5px" }}> Filter by: </h4>
      {/* Age Column */}
      <div style={{ border: "2px solid #800020", padding: "8px", marginBottom: "6px", maxHeight: "120px", overflowY: "auto", backgroundColor: "#b33655ff" }}>
        <label className="fw-bold text-decoration-underline" style={{ color: "white" }}>AGE GROUP</label>
        {[
          { value: "All ages", label: "All ages" },
          { value: "5-9", label: "5-9" },
          { value: "10-14", label: "10-14" }
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
          "SSS/SHS",
          "Secondary",
          "Voc/technical/commercial"
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

    {/* Status */}
      <div style={{ border: "2px solid #c42f54ff", padding: "8px", marginBottom: "6px", maxHeight: "120px", overflowY: "auto", backgroundColor: "#b33655ff"}}>
        <label className="fw-bold text-decoration-underline" style={{ color: "white" }}>ECONOMIC ACTIVE STATUS</label>
        {["Economically Active","Not Economically Active"].map((opt) => (
          <div className="form-check" key={opt}>
            <input
              className="form-check-input"
              type="radio"
              name="active_status"
              id={`active_status-${opt}`}
              value={opt}
              checked={filters.active_status === opt}
              onChange={(e) =>
                setFilters({ ...filters, active_status: e.target.value })
              }
            />
            <label className="form-check-label" htmlFor={`active_status-${opt}`} style={{ color: "white" }}>
              {opt}
            </label>
          </div>
        ))}
      </div>                         

    </div>
  );
}

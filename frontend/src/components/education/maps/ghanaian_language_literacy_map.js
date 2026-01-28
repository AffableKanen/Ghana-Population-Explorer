import React, { useEffect, useRef, useState } from "react";
import GhanaianLanguageLiteracyFilters from "../filters/filters_ghanaian_language_literacy";
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-search';
import 'leaflet-search/dist/leaflet-search.min.css';
import Plotly from 'plotly.js-dist-min';

function  GhanaianLanguageLiteracyMap() {
  const mapRef = useRef(null);
  const geoJsonLayerRef = useRef(null);
  const legendRef = useRef(null);
  const plotRef = useRef(null);
  const searchControlRef = useRef(null);

  const [filters, setFilters] = useState({
    age_column: "All ages",
    sex: "Both Sexes",
    locality: "All Locality Types", 
    education: "Total",
    language: "Akwapim_Twi"
  });

  // Initialize map once
  useEffect(() => {
    if (!mapRef.current) {
      mapRef.current = L.map("map").setView([0, 0], 6);

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "© OpenStreetMap contributors",
      }).addTo(mapRef.current); 
    }
  }, []); 



  // Function to fetch new data and update map
  const updateMap = async (newFilters) => {
    const res = await fetch("http://127.0.0.1:8000/ghanaian_language_literacy", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newFilters),
    });
    const data = await res.json();

    const values = data.features.map((f) => f.properties[filters.age_column]);

        // Quantiles
        function getQuantiles(values, numQuantiles) {
          values.sort((a, b) => a - b);
          let quantiles = [];
          for (let i = 1; i < numQuantiles; i++) {
            let pos = (values.length - 1) * (i / numQuantiles);
            let base = Math.floor(pos);
            let rest = pos - base;
            if (values[base + 1] !== undefined) {
              quantiles.push(
                values[base] + rest * (values[base + 1] - values[base])
              );
            } else {
              quantiles.push(values[base]);
            }
          }
          return quantiles;
        }

        const breaks = getQuantiles(values, 5);
        const colors = ["#fee5d9", "#fcae91", "#fb6a4a", "#f31a1a", "#8a0409"];

        const getColor = (value) => {
          if (value <= breaks[0]) return colors[0];
          else if (value <= breaks[1]) return colors[1];
          else if (value <= breaks[2]) return colors[2];
          else if (value <= breaks[3]) return colors[3];
          else return colors[4];
        };
    
    // Remove old GeoJSON layer if it exists
    if (geoJsonLayerRef.current) {
      mapRef.current.removeLayer(geoJsonLayerRef.current);
    }

    geoJsonLayerRef.current = L.geoJSON(data, {
          style: (feature) => ({
            fillColor: getColor(feature.properties[filters.age_column]),
            weight: 1,
            opacity: 1,
            color: "#393B07",
            fillOpacity: 0.9,
          }),

          onEachFeature: (feature, layer) => {
            // Hover popup
            layer.bindPopup(
              `District: ${feature.properties.District}<br>
              Region: ${feature.properties.Region}<br>
              Percentage With Difficulty: ${feature.properties[filters.age_column]}%`
            );



            // 👉 Click handler for zoom + plot
            layer.on("click", function (e) {

              // extract neighboring districts
                let neighbors_names = feature.properties.Neighbors.split(",");
                let values = [];

                data.features.forEach((f) => {
                  if (neighbors_names.includes(f.properties.District)) {
                    values.push(f.properties[filters.age_column]);
                  };
                });

              let neigh_average = values.reduce((sum, v) => sum + v, 0) / values.length;


              // ################################################################################################

              let plot_data1 = [
                {
                  x: [
                    feature.properties.District+' District',
                    'Neighborhood Average'
                  ],
                  y: [
                    feature.properties[filters.age_column],
                    neigh_average
                  ],
                  type: "bar",
                },
              ];

              const layout1 = {
                title: {
                  text: `${feature.properties.District} District vs <br> Neighborhood Average`,
                 font: {
                    family: 'Arial, sans-serif', // Set the font family
                    size: 16, // Set the font size 
                  }
                },
                xaxis: {
                  tickangle: 15
                },
                width: 325,
                height: 305
              };
// ##################################################################################################################################

              let plot_data2 = [
                {
                  x: [
                    feature.properties.District+' District',
                    feature.properties.Region+' Region'
                  ],
                  y: [
                    feature.properties[filters.age_column],
                    feature.properties.Regional_percentage
                  ],
                  type: "bar",
                },
              ];

              const layout2 = {
                title: {
                  text: `${feature.properties.District} District vs <br> ${feature.properties.Region} Region`,
                      font: {
                          family: 'Arial, sans-serif', // Set the font family
                          size: 16, // Set the font size 
                        }
                },
                xaxis: {
                  tickangle: 15
                },

                width: 325,
                height: 305
              };


              let plot_data3 = [
                {
                  x: [
                    feature.properties.District+' District',
                    'Ghana'
                  ],
                  y: [
                    feature.properties[filters.age_column],
                    feature.properties.National_percentage
                  ],
                  type: "bar",
                },
              ];

              const layout3 = {
                title: {
                  text: `${feature.properties.District} District vs <br> Ghana`,
                     font: {
                          family: 'Arial, sans-serif', // Set the font family
                          size: 16, // Set the font size 
                        }
                },
                xaxis: {
                  tickangle: 15
                },
                width: 325,
                height: 305
              };

              // Update plot only on click
              Plotly.newPlot("neighborhood_plot", plot_data1, layout1, {responsive: true} );
              Plotly.newPlot("regional_plot", plot_data2, layout2, {responsive: true} );
              Plotly.newPlot("national_plot", plot_data3, layout3, {responsive: true} );
            });
          },
}).addTo(mapRef.current);

// 👉 Add search control after GeoJSON layer exists
  if (searchControlRef.current) {
    mapRef.current.removeControl(searchControlRef.current); // remove old one
  }

  const searchControl = new L.Control.Search({
    layer: geoJsonLayerRef.current,
    propertyName: "District",
    marker: false,
    position: "topright",
    collapsed: false,
    textPlaceholder: "Search District...",
    moveToLocation: function (latlng, title, map) {
      map.setView(latlng, 10);
    },
  });

  let lastHighlightedLayer = null;
  searchControl.on("search:locationfound", function (e) {
    if (lastHighlightedLayer) {
      geoJsonLayerRef.current.resetStyle(lastHighlightedLayer);
    }
    e.layer.setStyle({ fillColor: "yellow", weight: 3, color: "red" });
    e.layer.openPopup();
    lastHighlightedLayer = e.layer;
  });

  searchControl.on("search:collapsed", function () {
    if (lastHighlightedLayer) {
      geoJsonLayerRef.current.resetStyle(lastHighlightedLayer);
      lastHighlightedLayer = null;
    }
  });

  
  mapRef.current.addControl(searchControl);
  searchControlRef.current = searchControl; // save ref

    // Fit bounds
    mapRef.current.fitBounds(geoJsonLayerRef.current.getBounds());

    if (legendRef.current) {
      mapRef.current.removeControl(legendRef.current);
    }
      // Legend
      const legend = L.control({ position: "bottomright" });
      legend.onAdd = function () {
        const div = L.DomUtil.create("div", "legend");
        div.style.backgroundColor = "white";
        div.style.padding = "10px";
        div.style.border = "1px solid #ccc";

        div.innerHTML = `<b>Percentage of ${filters.age_column} </b><br>`;
        div.innerHTML += `<div style="width: 20px; height: 20px; background-color: ${colors[0]}; display:inline-block; margin-right:5px;"></div>Less than ${breaks[0]}<br>`;
        div.innerHTML += `<div style="width: 20px; height: 20px; background-color: ${colors[1]}; display:inline-block; margin-right:5px;"></div>${breaks[0]} - ${breaks[1]}<br>`;
        div.innerHTML += `<div style="width: 20px; height: 20px; background-color: ${colors[2]}; display:inline-block; margin-right:5px;"></div>${breaks[1]} - ${breaks[2]}<br>`;
        div.innerHTML += `<div style="width: 20px; height: 20px; background-color: ${colors[3]}; display:inline-block; margin-right:5px;"></div>${breaks[2]} - ${breaks[3]}<br>`;
        div.innerHTML += `<div style="width: 20px; height: 20px; background-color: ${colors[4]}; display:inline-block; margin-right:5px;"></div>Above ${breaks[3]}<br>`;

        return div;
      };
      legend.addTo(mapRef.current);

      legendRef.current = legend;
  };


  // Update map whenever filters change 
  useEffect(() => {
    updateMap(filters);
  }, [filters]);

  return (
      <div className="container-fluid">
        <div className="row">
           <div
            className="col-2"
            style={{ backgroundColor: "#f4f4f4" }}
          >
            {/* pass the filter elements */}
            <GhanaianLanguageLiteracyFilters filters={filters} setFilters={setFilters} />
          </div>
  
          <div
            className="col-3"
            id="map"
            style={{ height: "690px" }}
          ></div>


          <div className="col-7">

            <div className="row" style={{backgroundColor:'white', height:"55%", marginTop: "10px", marginBottom:'10px', 
              marginLeft:"10px", marginRight:"10px", borderRadius:"5px", maxHeight:"350px"}}>

              <h3 style={{textAlign:"center"}}>Percentage of Persons With Difficulty by District</h3>

              <p style={{fontSize:"25px"}}>
                Disability Status is not defined for ages less than 5 Years, and With difficulty comprises persons who reported having some difficulty, 
                a lot of difficulty and cannot do it at all in at least one of the domains (seeing, hearing, walking or climbing stairs, remembering or 
                concentrating, self-care and communicating)
              </p>

            </div>

            <div className="row">
                    <div
                      className="col-4"
                      id="neighborhood_plot"
                      style={{ marginLeft: "5px" }}
                    >
                    </div>

                    <div
                      className="col-4"
                      id="regional_plot"
                      style={{ marginLeft: "5px" }}
                    >
                    </div>

                    <div
                      className="col-3"
                      id="national_plot"
                    >
                    </div>
            </div>

          </div>

        </div>
      </div>
    );
}

export default GhanaianLanguageLiteracyMap;


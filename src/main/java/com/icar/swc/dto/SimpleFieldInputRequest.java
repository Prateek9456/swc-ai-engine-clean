package com.icar.swc.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class SimpleFieldInputRequest {

    private Double lat;
    private Double lon;

    @JsonProperty("land_use") // 👈 THIS IS THE FIX
    private String landUse;

    public Double getLat() {
        return lat;
    }

    public void setLat(Double lat) {
        this.lat = lat;
    }

    public Double getLon() {
        return lon;
    }

    public void setLon(Double lon) {
        this.lon = lon;
    }

    public String getLandUse() {
        return landUse;
    }

    public void setLandUse(String landUse) {
        this.landUse = landUse;
    }
}

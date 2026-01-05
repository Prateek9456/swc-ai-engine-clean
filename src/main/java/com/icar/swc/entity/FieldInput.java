package com.icar.swc.entity;

import java.time.LocalDateTime;

import org.hibernate.annotations.CreationTimestamp;

import jakarta.persistence.*;

@Entity
@Table(name = "field_input")
public class FieldInput {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "land_slope")
    private Double landSlope;

    @Column(name = "soil_depth")
    private String soilDepth;

    @Column(name = "rainfall")
    private Double rainfall;

    @Column(name = "land_use")
    private String landUse;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    /* ===== GETTERS & SETTERS ===== */

    public Long getId() {
        return id;
    }

    public Double getLandSlope() {
        return landSlope;
    }

    public void setLandSlope(Double landSlope) {
        this.landSlope = landSlope;
    }

    public String getSoilDepth() {
        return soilDepth;
    }

    public void setSoilDepth(String soilDepth) {
        this.soilDepth = soilDepth;
    }

    public Double getRainfall() {
        return rainfall;
    }

    public void setRainfall(Double rainfall) {
        this.rainfall = rainfall;
    }

    public String getLandUse() {
        return landUse;
    }

    public void setLandUse(String landUse) {
        this.landUse = landUse;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
}

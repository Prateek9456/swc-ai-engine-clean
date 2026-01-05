package com.icar.swc.entity;

import java.time.LocalDateTime;

import org.hibernate.annotations.CreationTimestamp;

import jakarta.persistence.*;

@Entity
@Table(name = "decision_result")
public class DecisionResult {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne
    @JoinColumn(name = "field_input_id", nullable = false)
    private FieldInput fieldInput;

    @Lob
    @Column(name = "recommended_measures")
    private String recommendedMeasures;

    @Column(name = "confidence")
    private Double confidence;

    @Lob
    @Column(name = "explanation")
    private String explanation;

    @Column(name = "source")
    private String source; // RULE_ENGINE / AGENT_AI

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    /* ===== GETTERS & SETTERS ===== */

    public Long getId() {
        return id;
    }

    public FieldInput getFieldInput() {
        return fieldInput;
    }

    public void setFieldInput(FieldInput fieldInput) {
        this.fieldInput = fieldInput;
    }

    public String getRecommendedMeasures() {
        return recommendedMeasures;
    }

    public void setRecommendedMeasures(String recommendedMeasures) {
        this.recommendedMeasures = recommendedMeasures;
    }

    public Double getConfidence() {
        return confidence;
    }

    public void setConfidence(Double confidence) {
        this.confidence = confidence;
    }

    public String getExplanation() {
        return explanation;
    }

    public void setExplanation(String explanation) {
        this.explanation = explanation;
    }

    public String getSource() {
        return source;
    }

    public void setSource(String source) {
        this.source = source;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
}

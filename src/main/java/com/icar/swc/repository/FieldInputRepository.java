package com.icar.swc.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.icar.swc.entity.FieldInput;

public interface FieldInputRepository extends JpaRepository<FieldInput, Long> {
    // No custom queries for now
}

package com.icar.swc.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.icar.swc.entity.User;

public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByUsername(String username);
}

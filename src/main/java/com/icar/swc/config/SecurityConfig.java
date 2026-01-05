package com.icar.swc.config;

import java.time.LocalDateTime;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

import com.icar.swc.entity.User;
import com.icar.swc.repository.UserRepository;
import com.icar.swc.security.JwtAuthFilter;
import com.icar.swc.security.JwtService;

@Configuration
public class SecurityConfig {

    private final JwtService jwtService;
    private final JwtAuthFilter jwtAuthFilter;
    private final UserRepository userRepository;

    public SecurityConfig(
            JwtService jwtService,
            JwtAuthFilter jwtAuthFilter,
            UserRepository userRepository
    ) {
        this.jwtService = jwtService;
        this.jwtAuthFilter = jwtAuthFilter;
        this.userRepository = userRepository;
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {

        http
            // ✅ APIs are stateless
            .csrf(csrf -> csrf.disable())

            .authorizeHttpRequests(auth -> auth
                // ✅ PUBLIC / AUTH ROUTES
                .requestMatchers(
                    "/",
                    "/login",
                    "/register",
                    "/auth/**",
                    "/oauth2/**",
                    "/login/oauth2/**",
                    "/error"
                ).permitAll()

                // ✅ VERY IMPORTANT: ALLOW ALL API CALLS
                .requestMatchers("/api/**").permitAll()

                // 🔐 Everything else requires authentication
                .anyRequest().authenticated()
            )

            // ✅ GOOGLE LOGIN (UI ONLY)
            .oauth2Login(oauth2 -> oauth2
                .successHandler((request, response, authentication) -> {

                    OAuth2User oauthUser =
                            (OAuth2User) authentication.getPrincipal();

                    String email = oauthUser.getAttribute("email");

                    User user = userRepository.findByUsername(email)
                        .orElseGet(() -> {
                            User u = new User();
                            u.setUsername(email);
                            u.setPassword(null);
                            u.setProvider("GOOGLE");
                            u.setRole("USER");
                            u.setCreatedAt(LocalDateTime.now());
                            return userRepository.save(u);
                        });

                    String token =
                            jwtService.generateToken(user.getUsername());

                    response.sendRedirect(
                        "http://localhost:3000/oauth-success?token=" + token
                    );
                })
            )

            // ✅ JWT FILTER (for protected routes)
            .addFilterBefore(
                jwtAuthFilter,
                UsernamePasswordAuthenticationFilter.class
            )

            // ✅ LOGOUT
            .logout(logout -> logout
                .logoutSuccessUrl("http://localhost:3000/login")
                .permitAll()
            );

        return http.build();
    }
}

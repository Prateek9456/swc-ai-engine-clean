package com.icar.swc.config;

import java.time.LocalDateTime;
import java.util.List;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import com.icar.swc.entity.User;
import com.icar.swc.repository.UserRepository;
import com.icar.swc.security.JwtAuthFilter;
import com.icar.swc.security.JwtService;

@Configuration
public class SecurityConfig {

    // ✅ YOUR REAL FRONTEND URL
    private static final String FRONTEND_URL =
            "https://swc-ai-engine-clean.vercel.app";

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
            .csrf(csrf -> csrf.disable())
            .cors(cors -> cors.configurationSource(corsConfigurationSource()))

            .authorizeHttpRequests(auth -> auth
                // ✅ PUBLIC
                .requestMatchers(
                    "/",
                    "/error",
                    "/auth/**",
                    "/oauth2/**",
                    "/login/oauth2/**"
                ).permitAll()

                // ✅ FRONTEND → BACKEND APIs
                .requestMatchers("/api/**").permitAll()

                .anyRequest().authenticated()
            )

            // ✅ GOOGLE LOGIN
            .oauth2Login(oauth2 -> oauth2
                .successHandler((request, response, authentication) -> {

                    OAuth2User oauthUser =
                            (OAuth2User) authentication.getPrincipal();

                    String email = oauthUser.getAttribute("email");

                    User user = userRepository.findByUsername(email)
                        .orElseGet(() -> {
                            User u = new User();
                            u.setUsername(email);
                            u.setProvider("GOOGLE");
                            u.setRole("USER");
                            u.setCreatedAt(LocalDateTime.now());
                            return userRepository.save(u);
                        });

                    String token =
                            jwtService.generateToken(user.getUsername());

                    // 🔥 SEND TOKEN TO FRONTEND
                    response.sendRedirect(
                        FRONTEND_URL + "/oauth-success?token=" + token
                    );
                })
            )

            // ✅ JWT FILTER
            .addFilterBefore(
                jwtAuthFilter,
                UsernamePasswordAuthenticationFilter.class
            )

            // ✅ LOGOUT
            .logout(logout -> logout
                .logoutSuccessUrl(FRONTEND_URL + "/login")
                .permitAll()
            );

        return http.build();
    }

    // 🔥 REQUIRED FOR VERCEL → RENDER
    @Bean
    public CorsConfigurationSource corsConfigurationSource() {

        CorsConfiguration config = new CorsConfiguration();

        config.setAllowedOrigins(List.of(FRONTEND_URL));
        config.setAllowedMethods(List.of("GET","POST","PUT","DELETE","OPTIONS"));
        config.setAllowedHeaders(List.of("*"));
        config.setAllowCredentials(true);

        UrlBasedCorsConfigurationSource source =
                new UrlBasedCorsConfigurationSource();

        source.registerCorsConfiguration("/**", config);
        return source;
    }
}

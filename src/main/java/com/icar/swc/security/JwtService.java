package com.icar.swc.security;

import java.security.Key;
import java.util.Date;

import org.springframework.security.core.Authentication;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.stereotype.Service;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;

@Service
public class JwtService {

    // ⚠️ In production, move this to application.properties / env variable
    private static final String SECRET_KEY =
            "THIS_IS_A_VERY_SECURE_SECRET_KEY_CHANGE_IN_PRODUCTION_123456";

    private static final long EXPIRATION_TIME = 24 * 60 * 60 * 1000; // 24 hours

    /* =====================================================
       GENERATE JWT FROM USERNAME (NORMAL LOGIN)
    ===================================================== */
    public String generateToken(String username) {
        return Jwts.builder()
                .setSubject(username)
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + EXPIRATION_TIME))
                .signWith(getSignKey(), SignatureAlgorithm.HS256)
                .compact();
    }

    /* =====================================================
       GENERATE JWT FROM AUTHENTICATION (GOOGLE OAUTH)
    ===================================================== */
    public String generateToken(Authentication authentication) {

        String email;

        if (authentication.getPrincipal() instanceof OAuth2User oauthUser) {
            email = oauthUser.getAttribute("email");
        } else {
            email = authentication.getName();
        }

        return generateToken(email);
    }

    /* =====================================================
       VALIDATE TOKEN
    ===================================================== */
    public boolean validateToken(String token) {
        try {
            Jwts.parserBuilder()
                .setSigningKey(getSignKey())
                .build()
                .parseClaimsJws(token);
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    /* =====================================================
       EXTRACT USERNAME
    ===================================================== */
    public String extractUsername(String token) {
        return Jwts.parserBuilder()
                .setSigningKey(getSignKey())
                .build()
                .parseClaimsJws(token)
                .getBody()
                .getSubject();
    }

    /* =====================================================
       SIGNING KEY
    ===================================================== */
    private Key getSignKey() {
        return Keys.hmacShaKeyFor(SECRET_KEY.getBytes());
    }
}

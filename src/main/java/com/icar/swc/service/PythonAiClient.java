package com.icar.swc.service;

import java.util.HashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
public class PythonAiClient {

    private final RestTemplate restTemplate = new RestTemplate();

    // ✅ Flask URL injected from environment (Render-safe)
    @Value("${python.ai.base-url}")
    private String flaskUrl;

    public Map<String, Object> analyze(
            Double lat,
            Double lon,
            String landUse
    ) {

        // 🔥 LOG VALUES BEFORE SENDING
        System.out.println("PYTHON PAYLOAD VALUES:");
        System.out.println("lat = " + lat);
        System.out.println("lon = " + lon);
        System.out.println("landUse = " + landUse);
        System.out.println("Calling Flask URL: " + flaskUrl);

        Map<String, Object> payload = new HashMap<>();
        payload.put("lat", lat);
        payload.put("lon", lon);
        payload.put("land_use", landUse); // MUST be snake_case

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<Map<String, Object>> entity =
                new HttpEntity<>(payload, headers);

        ResponseEntity<Map> response =
                restTemplate.postForEntity(
                        flaskUrl,
                        entity,
                        Map.class
                );

        return response.getBody();
    }
}

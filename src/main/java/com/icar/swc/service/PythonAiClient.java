package com.icar.swc.service;

import java.util.HashMap;
import java.util.Map;

import org.springframework.http.*;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
public class PythonAiClient {

    private final RestTemplate restTemplate = new RestTemplate();

    public Map<String, Object> analyze(
            Double lat,
            Double lon,
            String landUse
    ) {
        String url = "http://127.0.0.1:5000/analyze";

        // 🔥 LOG VALUES BEFORE SENDING
        System.out.println("PYTHON PAYLOAD VALUES:");
        System.out.println("lat = " + lat);
        System.out.println("lon = " + lon);
        System.out.println("landUse = " + landUse);

        Map<String, Object> payload = new HashMap<>();
        payload.put("lat", lat);
        payload.put("lon", lon);
        payload.put("land_use", landUse); // MUST be snake_case

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<Map<String, Object>> entity =
                new HttpEntity<>(payload, headers);

        ResponseEntity<Map> response =
                restTemplate.postForEntity(url, entity, Map.class);

        return response.getBody();
    }
}

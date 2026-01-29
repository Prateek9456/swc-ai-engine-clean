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

    // ✅ Inject Flask URL from environment
    @Value("${python.ai.base-url}")
    private String flaskUrl;

    public Map<String, Object> analyze(
            Double lat,
            Double lon,
            String landUse
    ) {
        String url = flaskUrl + "/analyze";

        System.out.println("CALLING FLASK URL: " + url);

        Map<String, Object> payload = new HashMap<>();
        payload.put("lat", lat);
        payload.put("lon", lon);
        payload.put("land_use", landUse);

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<Map<String, Object>> entity =
                new HttpEntity<>(payload, headers);

        ResponseEntity<Map> response =
                restTemplate.postForEntity(url, entity, Map.class);

        return response.getBody();
    }
}

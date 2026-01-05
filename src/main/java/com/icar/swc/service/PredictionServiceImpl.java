package com.icar.swc.service;

import java.util.Map;

import org.springframework.stereotype.Service;

import com.icar.swc.dto.SimpleFieldInputRequest;

@Service
public class PredictionServiceImpl implements PredictionService {

    private final PythonAiClient pythonAiClient;

    public PredictionServiceImpl(PythonAiClient pythonAiClient) {
        this.pythonAiClient = pythonAiClient;
    }

    @Override
    public Map<String, Object> predict(SimpleFieldInputRequest request) {

        System.out.println("REQUEST DTO VALUES:");
        System.out.println("lat = " + request.getLat());
        System.out.println("lon = " + request.getLon());
        System.out.println("landUse = " + request.getLandUse());

        return pythonAiClient.analyze(
            request.getLat(),
            request.getLon(),
            request.getLandUse()
        );
    }

}

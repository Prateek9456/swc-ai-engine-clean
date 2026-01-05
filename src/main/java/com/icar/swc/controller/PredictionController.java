package com.icar.swc.controller;

import java.util.Map;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.icar.swc.dto.SimpleFieldInputRequest;
import com.icar.swc.service.PredictionService;

@RestController
@RequestMapping("/api")
public class PredictionController {

    private final PredictionService predictionService;

    public PredictionController(PredictionService predictionService) {
        this.predictionService = predictionService;
    }

    @PostMapping("/predict")
    public ResponseEntity<?> predict(@RequestBody SimpleFieldInputRequest req) {
        return ResponseEntity.ok(
            predictionService.predict(req)
        );
    }

}

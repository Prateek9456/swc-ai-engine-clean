package com.icar.swc.service;

import java.util.Map;
import com.icar.swc.dto.SimpleFieldInputRequest;

public interface PredictionService {

    Map<String, Object> predict(SimpleFieldInputRequest request);
}

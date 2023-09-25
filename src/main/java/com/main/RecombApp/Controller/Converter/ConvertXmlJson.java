package com.main.RecombApp.Controller.Converter;


import com.main.RecombApp.Payload.Request.NotaFiscalRequest;
import com.main.RecombApp.Payload.Response.NotaFiscalResponse;
import com.main.RecombApp.Services.Deserialize.DeserializeXML;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;

@RestController
@CrossOrigin
@RequestMapping("/convert/")
public class ConvertXmlJson {

    @Autowired
    DeserializeXML deserializeXML;

    // Just test
    @PostMapping("xmlToJson")
    public ResponseEntity<?> convertFile(@ModelAttribute NotaFiscalRequest notaFiscalRequest) throws IOException {
        return ResponseEntity.ok(deserializeXML.SaveXml(notaFiscalRequest.getFileNf()));
    }

}

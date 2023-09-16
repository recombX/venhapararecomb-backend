package com.main.RecombApp.Controller;

import com.main.RecombApp.Payload.Request.NotaFiscalRequest;
import com.main.RecombApp.Payload.Response.NotaFiscalResponse;
import com.main.RecombApp.Services.Deserialize.DeserializeXML;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

@RestController
@RequestMapping("/notafiscal")
@RequiredArgsConstructor
@CrossOrigin
public class NotaFiscalController {

    @Autowired
    DeserializeXML deserializeXML;

//    @GetMapping("/get")
//    public ResponseEntity<NotaFiscalResponse> GetAllNotaFiscal(){
//
//    }

    @PostMapping("/send")
    public ResponseEntity<?> SendNotaFiscal(@RequestParam MultipartFile NotaFiscalFile) throws IOException {
        deserializeXML.SaveXml(NotaFiscalFile);
        return ResponseEntity.ok().body("TESTE");
    }
}

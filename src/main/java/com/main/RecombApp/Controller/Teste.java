package com.main.RecombApp.Controller;

import com.main.RecombApp.Services.Deserialize.DeserializeXML;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

@RestController
@RequestMapping("/teste")
@RequiredArgsConstructor
@CrossOrigin
public class Teste {

    @Autowired
    DeserializeXML deserializeXML;

//    @GetMapping("/get")
//    public ResponseEntity<NotaFiscalResponse> GetAllNotaFiscal(){
//
//    }

    @PostMapping("/teste")
    public ResponseEntity<?> SendNotaFiscal() throws IOException {
        return ResponseEntity.ok().body("OKAY");
    }
}

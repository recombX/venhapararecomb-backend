package com.main.RecombApp.Controller;

import com.main.RecombApp.Payload.Request.NotaFiscalRequest;
import com.main.RecombApp.Payload.Response.NFResponse;
import com.main.RecombApp.Payload.Response.NotaFiscalResponse;
import com.main.RecombApp.Services.Deserialize.DeserializeXML;
import com.main.RecombApp.Services.NotaFiscal.NotaFiscalService;
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
    @Autowired
    NotaFiscalService notaFiscalService;

    @GetMapping("/get")
    public ResponseEntity<?> GetAllNotaFiscal(@RequestParam String Documento){
        return ResponseEntity.ok().body("OK");
    }

    @GetMapping("/{documento}")
    public ResponseEntity<NFResponse> ClienteFornecedorCPF(@PathVariable String documento)
    {
        return  ResponseEntity.ok().body(notaFiscalService.GetFornecedorClienteCPF(documento));
    }
}

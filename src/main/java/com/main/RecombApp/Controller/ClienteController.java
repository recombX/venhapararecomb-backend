package com.main.RecombApp.Controller;

import ch.qos.logback.core.net.server.Client;
import com.main.RecombApp.Model.Cliente;
import com.main.RecombApp.Payload.Response.ClienteResponse;
import com.main.RecombApp.Services.Cliente.ClienteService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;


import java.util.List;

@RestController
@RequestMapping("/cliente")
@RequiredArgsConstructor
@CrossOrigin
public class ClienteController {

    @Autowired
    ClienteService clienteService;

    @GetMapping("/getAll")
    public ResponseEntity<List<Cliente>> findAllClients() {
        return ResponseEntity.ok().body(clienteService.findAllClients());
    }

    @GetMapping("/{documento}")
    public ResponseEntity<ClienteResponse> FindClientValue(@PathVariable String documento){
        var a = clienteService.findClientByValues(documento);
        return ResponseEntity.ok().body(clienteService.findClientByValues(documento));
    }

}

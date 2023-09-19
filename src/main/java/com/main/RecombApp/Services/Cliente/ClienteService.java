package com.main.RecombApp.Services.Cliente;

import com.main.RecombApp.Model.Cliente;
import com.main.RecombApp.Payload.Response.ClienteResponse;
import com.main.RecombApp.Repository.ClienteRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ClienteService {
    @Autowired
    ClienteRepository clienteRepository;

    public List<Cliente> findAllClients(){
        return clienteRepository.findAll();
    }

    public ClienteResponse findClientByValues(String valor){
        return ClienteResponse.builder().clientes(clienteRepository.findAllByCPFStartsWith(valor)).build();
    }

}

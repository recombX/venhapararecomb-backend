package com.main.RecombApp.Services.NotaFiscal;

import com.main.RecombApp.Payload.Response.NFResponse;
import com.main.RecombApp.Repository.BoletoRepository;
import com.main.RecombApp.Repository.ClienteRepository;
import com.main.RecombApp.Repository.FornecedorRepository;
import com.main.RecombApp.Services.Cliente.ClienteService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.stereotype.Service;

@Service
public class NotaFiscalService {

    @Autowired
    BoletoRepository boletoRepository;

    @Autowired
    ClienteRepository clienteRepository;
    @Autowired
    FornecedorRepository fornecedorRepository;

    public NFResponse GetFornecedorClienteCPF(String documento){
        return NFResponse.builder().fornecedores(fornecedorRepository.findFornecedorsByCNPJStartsWith(documento)).clientes(clienteRepository.findAllByCPFStartsWith(documento)).build();
    }

}

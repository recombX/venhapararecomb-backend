package com.main.RecombApp.Services.Deserialize;


import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.dataformat.xml.XmlMapper;
import com.main.RecombApp.DTO.BoletoDTO;
import com.main.RecombApp.DTO.ClienteDTO;
import com.main.RecombApp.DTO.EnderecoDTO;
import com.main.RecombApp.DTO.FornecedorDTO;
import com.main.RecombApp.Model.Boleto;
import com.main.RecombApp.Model.Cliente;
import com.main.RecombApp.Model.Endereco;
import com.main.RecombApp.Model.Fornecedor;
import com.main.RecombApp.Payload.Response.NotaFiscalResponse;
import com.main.RecombApp.Repository.BoletoRepository;
import com.main.RecombApp.Repository.ClienteRepository;
import com.main.RecombApp.Repository.EnderecoRepository;
import com.main.RecombApp.Repository.FornecedorRepository;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Service
public class DeserializeXML {

    @Autowired
    EnderecoRepository enderecoRepository;
    @Autowired
    ClienteRepository clienteRepository;
    @Autowired
    FornecedorRepository fornecedorRepository;
    @Autowired
    BoletoRepository boletoRepository;

    public NotaFiscalResponse SaveXml(MultipartFile xmlFile) throws IOException {
        XmlMapper xmlMapper = new XmlMapper();
        JsonNode node = xmlMapper.readTree(xmlFile.getBytes());
        ModelMapper modelMapper = new ModelMapper();

        EnderecoDTO enderecoDTO = EnderecoDTO.builder()
                .CEP(node.at("/NFe/infNFe/dest/enderDest").get("CEP").asText())
                .cMun(node.at("/NFe/infNFe/dest/enderDest").get("cMun").asText())
                .cPais(node.at("/NFe/infNFe/dest/enderDest").get("cPais").asText())
                .xMun(node.at("/NFe/infNFe/dest/enderDest").get("xMun").asText())
                .nro(node.at("/NFe/infNFe/dest/enderDest").get("nro").asText())
                .UF(node.at("/NFe/infNFe/dest/enderDest").get("UF").asText())
                .xLgr(node.at("/NFe/infNFe/dest/enderDest").get("xLgr").asText())
                .xBairro(node.at("/NFe/infNFe/dest/enderDest").get("xBairro").asText())
                .xPais(node.at("/NFe/infNFe/dest/enderDest").get("xPais").asText())
                .fone(node.at("/NFe/infNFe/dest/enderDest").get("fone").asText())
                .build();


        // Mapper
        Endereco enderecoDTOModel = modelMapper.map(enderecoDTO, Endereco.class);

        if (enderecoRepository.findEnderecoByCEP(node.at("/NFe/infNFe/dest/enderDest").get("CEP").asText()) != null) {
            enderecoDTOModel = enderecoRepository.findEnderecoByCEP(node.at("/NFe/infNFe/dest/enderDest").get("CEP").asText());
        } else {
            enderecoRepository.save(enderecoDTOModel);
        }

        ClienteDTO clienteDTO = ClienteDTO.builder()
                .CPF(node.at("/NFe/infNFe/dest").get("CNPJ").asText())
                .nome(node.at("/NFe/infNFe/dest").get("xNome").asText())
                .endereco(enderecoDTOModel)
                .build();

        Cliente clienteDTOModel = modelMapper.map(clienteDTO, Cliente.class);

        if (clienteRepository.findByCPF(node.at("/NFe/infNFe/dest").get("CNPJ").asText()) == null) {
            clienteRepository.save(clienteDTOModel);
        }

        FornecedorDTO fornecedorDTO = FornecedorDTO.builder()
                .CNPJ(node.at("/NFe/infNFe/emit").get("CNPJ").asText())
                .nome(node.at("/NFe/infNFe/emit").get("xNome").asText())
                .build();

        Fornecedor fornecedorDTOModel = modelMapper.map(fornecedorDTO, Fornecedor.class);

        if (fornecedorRepository.findByCNPJ(node.at("/NFe/infNFe/emit").get("CNPJ").asText()) == null) {
            fornecedorRepository.save(fornecedorDTOModel);
        }

        // Considera-se que pode haver mais de um "parcelamento" do boleto
        List<BoletoDTO> listaBoletos = new ArrayList<>();

        for (int i = 0; i < node.at("/NFe/infNFe/cobr/dup").findValuesAsText("dVenc").size(); i++) {
            listaBoletos.add(BoletoDTO.builder()
                    .DataVencimento(node.at("/NFe/infNFe/cobr/dup").findValuesAsText("dVenc").get(i))
                    .ValorParcelado(node.at("/NFe/infNFe/cobr/dup").findValuesAsText("vDup").get(i))
                    .Value(node.at("/NFe/infNFe/cobr/fat").get("vLiq").asText())
                    .build());
        }

        for (BoletoDTO boletoDTO : listaBoletos) {
            Boleto boletoDTOModel = modelMapper.map(boletoDTO, Boleto.class);
            boletoRepository.save(boletoDTOModel);
        }

        return NotaFiscalResponse.builder()
                .fornecedor(fornecedorDTO)
                .cliente(clienteDTO)
                .boleto(listaBoletos)
                .build();
    }
}
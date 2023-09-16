package com.main.RecombApp.Services.Deserialize;


import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.dataformat.xml.XmlMapper;
import com.main.RecombApp.DTO.BoletoDTO;
import com.main.RecombApp.DTO.ClienteDTO;
import com.main.RecombApp.DTO.EnderecoDTO;
import com.main.RecombApp.DTO.FornecedorDTO;
import com.main.RecombApp.Model.Cliente;
import com.main.RecombApp.Model.Endereco;
import com.main.RecombApp.Payload.Response.NotaFiscalResponse;
import com.main.RecombApp.Repository.ClienteRepository;
import com.main.RecombApp.Repository.EnderecoRepository;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

@Service
public class DeserializeXML {

    @Autowired
    EnderecoRepository enderecoRepository;
    @Autowired
    ClienteRepository clienteRepository;

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


        return NotaFiscalResponse.builder()
                .fornecedor(FornecedorDTO.builder()
                        .CNPJ(node.at("/NFe/infNFe/emit").get("CNPJ").asText())
                        .nome(node.at("/NFe/infNFe/emit").get("xNome").asText())
                        .build())
                .cliente(clienteDTO)
                .boleto(BoletoDTO.builder()
                        .DataVencimento(node.at("/NFe/infNFe/cobr/dup").findValuesAsText("dVenc"))
                        .Value(node.at("/NFe/infNFe/cobr/fat").get("vLiq").asDouble())
                        .build())
                .build();
    }
}

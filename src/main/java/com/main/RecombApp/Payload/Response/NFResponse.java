package com.main.RecombApp.Payload.Response;

import com.main.RecombApp.DTO.BoletoDTO;
import com.main.RecombApp.DTO.ClienteDTO;
import com.main.RecombApp.DTO.FornecedorDTO;
import com.main.RecombApp.Model.Cliente;
import com.main.RecombApp.Model.Fornecedor;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class NFResponse {

    List<Cliente> clientes;
    List<Fornecedor> fornecedores;

}

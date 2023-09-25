package com.main.RecombApp.DTO;

import com.main.RecombApp.Model.Boleto;
import com.main.RecombApp.Model.Endereco;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Set;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ClienteDTO {

    private String CPF;
    private String nome;
    private Endereco endereco;
    Set<Boleto> boletos;

}

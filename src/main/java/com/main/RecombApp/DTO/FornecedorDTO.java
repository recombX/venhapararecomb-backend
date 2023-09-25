package com.main.RecombApp.DTO;

import com.main.RecombApp.Model.Endereco;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class FornecedorDTO {

    private String CNPJ;
    private String nome;
    private Endereco EnderecoEmissor;
}

package com.main.RecombApp.Model;


import jakarta.annotation.sql.DataSourceDefinition;
import jakarta.persistence.*;
import lombok.*;
import jakarta.validation.constraints.NotBlank;

@Table(name = "emitter")
@Entity
@Getter
@Setter
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
// Considerando Endereco como linhas do proprio emissor, porem, o correto e uma table de relacionamento
public class EmitterModel {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @NotBlank
    private String cnpj;
    @NotBlank
    private String xNome;
    @NotBlank
    private String xFant;
    @NotBlank
    private String xLgr;
    @NotBlank
    private String xBairro;
    @NotBlank
    private String cMun;
    @NotBlank
    private String uf;
    @NotBlank
    private String cep;
    @NotBlank
    private String cPais;
    @NotBlank
    private String xPais;
    @NotBlank
    private String telefone;

}

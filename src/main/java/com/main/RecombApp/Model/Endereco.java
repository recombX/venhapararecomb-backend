package com.main.RecombApp.Model;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import lombok.*;

@Table(name = "endereco")
@Entity
@Getter
@Setter
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Endereco {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank
    private String xLgr;
    @NotBlank
    private String nro;
    @NotBlank
    private String xBairro;
    @NotBlank
    private String cMun;
    @NotBlank
    private String xMun;
    @NotBlank
    private String UF;
    @NotBlank
    private String CEP;
    @NotBlank
    private String cPais;
    @NotBlank
    private String xPais;
    private String fone;


}

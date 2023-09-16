package com.main.RecombApp.DTO;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class BoletoDTO {

    private String Value;
    private String DataVencimento;
    private String ValorParcelado;

}

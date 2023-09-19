package com.main.RecombApp.Model;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import lombok.*;

import java.util.Set;

@Table(name = "boleto")
@Entity
@Getter
@Setter
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Boleto {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @NotBlank
    private String Value;
    @NotBlank
    private String ValorParcelado;
    @NotBlank
    private String DataVencimento;

    @ManyToMany
    @JoinTable(
            name = "clientefornecedor_boleto",
            joinColumns = @JoinColumn(name = "boleto_id"),
            inverseJoinColumns = @JoinColumn(name = "cliente_id"))
    Set<Boleto> boletos;
}

package com.main.RecombApp.Repository;

import com.main.RecombApp.DTO.EnderecoDTO;
import com.main.RecombApp.Model.Endereco;
import org.springframework.data.jpa.repository.JpaRepository;

public interface EnderecoRepository extends JpaRepository<Endereco, Long> {
    Endereco findEnderecoByCEP(String CEP);
}

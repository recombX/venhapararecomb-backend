package com.main.RecombApp.Repository;

import com.main.RecombApp.Model.Cliente;
import com.main.RecombApp.Model.Endereco;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ClienteRepository extends JpaRepository<Cliente, Long> {
    Cliente findByCPF(String CPF);
}

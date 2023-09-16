package com.main.RecombApp.Repository;

import com.main.RecombApp.Model.Cliente;
import com.main.RecombApp.Model.Fornecedor;
import org.springframework.data.jpa.repository.JpaRepository;

public interface FornecedorRepository extends JpaRepository<Fornecedor, Long> {
    Fornecedor findByCNPJ (String CPF);
}

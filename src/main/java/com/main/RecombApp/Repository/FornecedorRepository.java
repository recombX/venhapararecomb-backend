package com.main.RecombApp.Repository;

import com.main.RecombApp.Model.Cliente;
import com.main.RecombApp.Model.Fornecedor;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface FornecedorRepository extends JpaRepository<Fornecedor, Long> {
    Fornecedor findByCNPJ (String CPF);
    List<Fornecedor> findFornecedorsByCNPJStartsWith(String Cnpj);
}

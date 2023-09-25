package com.main.RecombApp.Repository;

import com.main.RecombApp.Model.Cliente;
import com.main.RecombApp.Model.Endereco;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ClienteRepository extends JpaRepository<Cliente, Long> {
    Cliente findByCPF(String CPF);
    List<Cliente> findAllByCPFStartsWith(String cpf);
}

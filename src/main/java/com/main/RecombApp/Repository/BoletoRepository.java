package com.main.RecombApp.Repository;

import com.main.RecombApp.Model.Boleto;
import com.main.RecombApp.Model.Cliente;
import org.springframework.data.jpa.repository.JpaRepository;

public interface BoletoRepository extends JpaRepository<Boleto, Long> {
}

package com.main.RecombApp.Repository;

import com.main.RecombApp.Model.Boleto;
import com.main.RecombApp.Model.Cliente;
import org.springframework.data.jdbc.repository.config.EnableJdbcRepositories;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface BoletoRepository extends JpaRepository<Boleto, Long> {


}

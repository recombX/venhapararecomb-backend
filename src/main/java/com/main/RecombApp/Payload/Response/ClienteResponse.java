package com.main.RecombApp.Payload.Response;

import com.main.RecombApp.Model.Cliente;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.ArrayList;
import java.util.List;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ClienteResponse {
    List<Cliente> clientes = new ArrayList<>();
}

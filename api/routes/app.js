const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const User = require('../models/User');
var cors = require('cors')
app.use(cors())

app.use(bodyParser.json());

app.post("/", async (req, res) => {
  try {
    await User.create(req.body);
    res.json({
      mensagem: "Cliente cadastrado com sucesso"
    });
  } catch (error) {
    console.error(error);
    res.status(400).json({
      mensagem: "Erro: Cliente não cadastrado"
    });
  }
});


app.get('/databaseEmpresa', async (_, res) => {
  try {
    const databaseEmpresa = await User.findAll({
      attributes: ['CNPJ', 'xNome', 'vNF', 'dVenc', 'xLgr', 'nro', 'xBairro', 'xMun', 'UF', 'CEP'],
    });

    if (databaseEmpresa) {
      res.json(databaseEmpresa);
    } else {
      res.status(404).json({ error: 'Nenhum dado encontrado' });
    }
  } catch (error) {
    console.error('Erro ao obter dados do banco de dados:', error);
    res.status(500).json({ error: 'Erro ao obter dados do banco de dados' });
  }
});


app.listen(8080, () => {
  console.log("Iniciando na porta 8080: http://localhost:8080");
});
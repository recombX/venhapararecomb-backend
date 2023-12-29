const Sequelize = require('sequelize');
const db = require('./db');

const User = db.define('users', {
    CNPJ: {
        type: Sequelize.STRING,
        allowNull: false,
        primaryKey: true 
    },
    xNome: {
        type: Sequelize.STRING,
        allowNull: false,
    },
    vNF: {
        type: Sequelize.FLOAT,
        allowNull: false,
    },
    dVenc: {
        type: Sequelize.STRING,
        allowNull: false,
    },
    xLgr: {
        type: Sequelize.STRING,
        allowNull: false,
    },
    nro: {
        type: Sequelize.STRING,
        allowNull: false,
    },
    xBairro: {
        type: Sequelize.STRING,
        allowNull: false,
    },
    xMun: {
        type: Sequelize.STRING,
        allowNull: false,
    },
    UF: {
        type: Sequelize.STRING,
        allowNull: false,
    },
    CEP: {
        type: Sequelize.STRING,
        allowNull: false,
    },
});

//Criar a tabela
User.sync();

module.exports = User;
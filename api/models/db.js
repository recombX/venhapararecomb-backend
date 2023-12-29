const Sequelize = require('sequelize');

const sequelize = new Sequelize( {
    dialect: 'sqlite',
    storage: '../databaseEmpresa.db'
});

module.exports = sequelize;

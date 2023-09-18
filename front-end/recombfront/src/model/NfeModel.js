export default class NfeModel
{
    boleto = [{
        value: null,
        valorParcelado: null,
        dataVencimento: null
    }];
    cliente = [{
        nome: "",
        endereco: [{

        }]
    }];

    constructor(boleto: [{ valorParcelado: null, dataVencimento: null, value: null }], cliente: [{ endereco: [{}], nome: string }]) {
        this.boleto = boleto;
        this.cliente = cliente;
    }
}
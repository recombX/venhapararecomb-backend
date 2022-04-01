# Biblioteca para trabalhar com XML
import xml.etree.ElementTree as ET

class NotaFiscal:
    def __init__(self, input_path: str):
        self.xml_path : str = input_path
        self.namespace: str = None
        self.root : ET.Element = self.xml_to_ElementTree(input_path)

    def __str__(self) -> str:
        str = ET.tostring(self.root, encoding='utf8').decode('utf8')
        return str

    # Extrai ElementTree da XML
    # ElementTree é uma árvore de elementos que representa do XML
    # 'elemet' ou 'elemento' da árvore será utilizado para referênciar
    # os galhoes ou folhas da árvore principal guardada em self.root
    def xml_to_ElementTree(self,input_path: str) -> ET.Element:
        try:
            root_with_namespace : ET.Element = ET.iterparse(input_path)
        except:
            print('Erro no XML ', input_path )
            exit(1)
        root : ET.Element = self.remove_namespace_from_nota_fiscal(root_with_namespace)
        return root

    # Retorna ElementTree sem nameSpace
    def remove_namespace_from_nota_fiscal(self, input: ET.Element) -> ET.Element:
        
        try:
            for _, el in input:
                prefix, has_namespace, postfix = el.tag.partition('}')
                if has_namespace:
                    if postfix == 'NFe':
                        self.set_namespace_nota_fiscal(has_namespace)
                    el.tag = postfix  # strip all namespaces
        except:
            print('Erro no XML ', self.xml_path )
            exit(1)

        root : ET.Element = input.root
        return root

    # Guarda Namespace da nota fiscal
    def set_namespace_nota_fiscal(self, namespace: str) -> None:
        self.namespace = namespace

    # --------- Emitente ---------

    # Retorna nome do destinatário
    def get_emit_name(self) -> str:
        name = self.get_text_from_xml_tree_element('./NFe/infNFe/emit/xNome')
        return name

    # Retorna cnpj do emissor da nota fiscal caso o 
    # mesmo seja uma pessoa jurídica
    def get_emit_cnpj(self) -> str:
        cnpj = self.get_text_from_xml_tree_element('./NFe/infNFe/emit/CNPJ')
        return cnpj
    
    # Retorna cpf do emissor da nota fiscal caso o 
    # mesmo seja uma pessoa física
    def get_emit_cpf(self) -> str:
        cpf = self.get_text_from_xml_tree_element('./NFe/infNFe/emit/CPF')
        return cpf
    
    # Retorna identificador do emissor
    def get_emit_identifier(self) -> str:
        cnpj = self.get_emit_cnpj()
        if(cnpj):
            return cnpj
        else:
            return self.get_emit_cpf()

    # Retorna endereço do emissor
    def get_emit_enderEmit(self) -> dict:
        enderEmit = self.get_dict_from_xml_tree_element('./NFe/infNFe/emit/enderEmit')
        return enderEmit
        
    # --------- Destinador ---------    

    # Retorna cnpj do destinatário da nota fiscal caso o 
    # mesmo seja uma pessoa jurídica
    def get_dest_cnpj(self) -> str:
        cnpj = self.get_text_from_xml_tree_element('./NFe/infNFe/dest/CNPJ')
        return cnpj

    # Retorna cpf do destinatário da nota fiscal caso o 
    # mesmo seja uma pessoa física
    def get_dest_cpf(self) -> str:
        cnpj = self.get_text_from_xml_tree_element('./NFe/infNFe/dest/CPF')
        return cnpj

    # Retorna identificador do destinatário
    def get_dest_identifier(self) -> str:
        cnpj = self.get_dest_cnpj()
        if(cnpj):
            return cnpj
        else:
            return self.get_dest_cpf()

    # Retorna nome do destinatário
    def get_dest_name(self) -> str:
        name = self.get_text_from_xml_tree_element('./NFe/infNFe/dest/xNome')
        return name
    
    # --------- Endereço ---------

    # Retorna endereço do destinatário
    def get_dest_enderDest(self) -> dict:
        enderDest = self.get_dict_from_xml_tree_element('./NFe/infNFe/dest/enderDest')
        enderDest['destinador_endereco_id'] = self.get_dest_cnpj()
        enderDest['destinador_id'] = self.get_dest_cnpj()

        return enderDest

    # --------- Dados para identificação da nota fiscal ---------
    def get_nota_fiscal_id(self) -> str:
        xml_tree_element = self.root.find('./NFe/infNFe')
        return xml_tree_element.attrib['Id']
    
    def get_nota_fiscal_valor_total(self) -> str:
        name = self.get_text_from_xml_tree_element('./NFe/infNFe/pag/detPag/vPag')
        return name

    # --------- Fatura ---------
    
    # Retorna lista de faturas contidas em uma 
    # nota fiscal
    def get_faturas(self) -> dict:
        faturas = []
        for tree_element_fatura in self.root.findall('./NFe/infNFe/cobr/dup'):
            fatura = {}
            fatura['duplicata_id'] = tree_element_fatura.find('nDup').text + self.get_nota_fiscal_id()
            fatura['nota_fiscal_id'] = self.get_nota_fiscal_id()
            fatura['data_vencimento'] = tree_element_fatura.find('dVenc').text
            fatura['valor_pago'] = tree_element_fatura.find('vDup').text
            faturas.append(fatura)
        return faturas

    # --------- Specific methods ---------

    # Retorna data de vencimento da nota fiscal
    def get_data_vencimento(self) -> str:
        data_vencimento = self.get_text_from_xml_tree_element('./NFe/infNFe/cobr/dup/dVenc')
        return data_vencimento
    
    # Retorna valor total da nota fiscal 
    # (impostos + valor unitário*unidades de cada produto)
    def get_valor_total(self) -> str:
        valor_total_nota = self.get_text_from_xml_tree_element('./NFe/infNFe/total/ICMSTot/vNF')
        return valor_total_nota

    # Exibe faturas da nota fiscal
    # Listar os valores e data de Vencimento dos boletos 
    # presentes em um nota fiscal
    def print_fatura(self) -> None:
        faturas = self.get_faturas()
        for fatura in faturas:
            print("Valor: R$", fatura['vDup'])
            print("Data de cencimento: ", fatura['dVenc'])
    
    # --------- UTILS ---------

    # Retorna o texto de um determinado elemento
    def get_text_from_xml_tree_element(self, tree_path: str) -> str:
        xml_tree_element = self.root.find(tree_path)
        if xml_tree_element != None:
            return xml_tree_element.text
        return None
    
    # Retorna retorna dicionário equivalente
    # a um elemento
    def get_dict_from_xml_tree_element(self, tree_path: str) -> dict:
        result_dict = {}
        xml_tree_element = self.root.find(tree_path)
        for chield in xml_tree_element:
            result_dict[chield.tag] = chield.text
        return result_dict

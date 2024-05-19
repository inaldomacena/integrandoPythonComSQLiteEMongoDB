from sqlite3 import Cursor

from dominio import Cliente, PessoaFisica, PessoaJuridica


class ClienteServico:
    def __init__(self, cursor: Cursor) -> None:
        self.cursor = cursor

    def filtrar_cliente(self, documento: str) -> int:
        if len(documento) == 11:
            self.cursor.execute("SELECT COUNT(*) AS total FROM pessoaFisica WHERE cpf=?;", (documento,))
        else:
            self.cursor.execute("SELECT COUNT(*) AS total FROM pessoaJuridica WHERE cnpj=?;", (documento,))
        return self.cursor.fetchone()["total"]

    def _criar_cliente_pessoa_fisica(self, documento: str) -> PessoaFisica:
        nome = input("Informe o nome completo: ")
        rendaMensal = float(input("Informe sua renda mensal: "))
        email = input("Informe seu email: ")
        telefone = input("Informe seu telefone: ")

        return PessoaFisica(
            nome=nome, cpf=documento, renda_mensal=renda_mensal, email=email, telefone=telefone, status="ativo"
        )

    def _criar_cliente_pessoa_juridica(self, documento: str) -> PessoaJuridica:
        nome = input("Informe o nome fantasia: ")
        faturamentoAnual = float(input("Informe seu faturamento anual: "))
        email = input("Informe seu email: ")
        telefone = input("Informe seu telefone: ")

        return PessoaJuridica(
            nomeFantasia=nome,
            cnpj=documento,
            faturamentoAnual=faturamentoAnual,
            email=email,
            telefone=telefone,
            status="ativo",
        )

    def _criar_cliente(self, cliente: Cliente) -> int:
        self.cursor.execute(
            "INSERT INTO cliente (email, telefone, status) VALUES (?,?,?);",
            (cliente.email, cliente.telefone, cliente.status),
        )
        return self.cursor.lastrowid

    def criar_cliente(self) -> None:
        documento = input("Informe o documento (CPF/CNPJ): ")
        existe_cliente = self.filtrar_cliente(documento)

        if existe_cliente:
            print("\n@@@ Já existe cliente com esse documento (CPF/CNPJ)! @@@")
            return

        if len(documento) == 11:
            cliente = self._criar_cliente_pessoa_fisica(documento=documento)
            cliente_id = self._criar_cliente(cliente=cliente)
            self.cursor.execute(
                "INSERT INTO pessoa_fisica (cliente_id, nome, cpf, renda_mensal) VALUES (?,?,?,?)",
                (cliente_id, cliente.nome, cliente.cpf, cliente.renda_mensal),
            )
        else:
            cliente = self._criar_cliente_pessoa_juridica(documento=documento)
            cliente_id = self._criar_cliente(cliente=cliente)
            self.cursor.execute(
                "INSERT INTO pessoaJuridica (cliente_id, nome_fantasia, cnpj, faturamentoAnual) VALUES (?,?,?,?)",
                (cliente_id, cliente.nomeFantasia, cliente.cnpj, cliente.faturamentoAnual),
            )

        print("\n=== Cliente criado com sucesso! ===")

    def listar_clientes(self) -> None:
        self.cursor.execute("SELECT * FROM pessoaFisica pf INNER JOIN cliente c ON c.id = pf.cliente_id;")
        clientes = self.cursor.fetchall()
        self.cursor.execute("SELECT * FROM pessoaJuridica pj INNER JOIN cliente c ON c.id = pj.cliente_id;")
        clientes += self.cursor.fetchall()

        if not clientes:
            print("\n@@@ Não existem clientes cadastrados! @@@")

        for cliente in clientes:
            print(self._apresentar_dados(dados_cliente=dict(cliente)))

    def _apresentar_dados(self, dados_cliente: dict[str, str | int]) -> str:
        if "cpf" in dados_cliente:
            return PessoaFisica.converter_objeto_bd(objeto_db=dados_cliente)
        return PessoaJuridica.converter_objeto_bd(objeto_db=dados_cliente)
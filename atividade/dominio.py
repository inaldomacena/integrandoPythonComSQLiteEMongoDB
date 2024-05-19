from dataclasses import dataclass
from typing import Self


@dataclass
class Cliente:
    email: str
    telefone: str
    status: str

    def __str__(self) -> str:
        texto = ""
        for campo, valor in self.__dict__.items():
            campo = campo.replace("_", " ").capitalize()
            texto += f"{campo}: {valor}\n"
        return texto


@dataclass
class PessoaFisica(Cliente):
    nome: str
    cpf: str
    rendaMensal: float

    @classmethod
    def converter_objeto_bd(cls, objeto_db: dict) -> Self:
        return cls(
            email=objeto_db["email"],
            telefone=objeto_db["telefone"],
            status=objeto_db["status"],
            nome=objeto_db["nome"],
            cpf=objeto_db["cpf"],
            rendaMensal=objeto_db["rendaMensal"],
        )


@dataclass
class PessoaJuridica(Cliente):
    nomeFantasia: str
    cnpj: str
    faturamentoAnual: float

    @classmethod
    def converter_objeto_bd(cls, objeto_db: dict) -> Self:
        return cls(
            email=objeto_db["email"],
            telefone=objeto_db["telefone"],
            status=objeto_db["status"],
            nomeFantasia=objeto_db["nomeFantasia"],
            cnpj=objeto_db["cnpj"],
            faturamentoAnual=objeto_db["faturamentoAnual"],
        )
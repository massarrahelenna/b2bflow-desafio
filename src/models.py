"""
modelo de dados pra contato
"""
from dataclasses import dataclass

@dataclass (frozen=True)
class Contato:
    nome:str
    telefone:str
    
    @staticmethod
    def from_dict(data: dict) -> 'Contato':
        return Contato(
            nome=str(data['nome']).strip(),
            telefone=str(data['telefone']).strip()
        )

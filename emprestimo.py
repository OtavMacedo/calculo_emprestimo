from datetime import datetime
from dateutil.relativedelta import relativedelta


class Emprestimo:
    def __init__(self,
                valor_emprestimo: float,
                tempo_anos: int,
                data_inicial_str: str,
                taxa_juros: float | None = None
    ) -> None:
        """
        Inicializa a classe Emprestimo com o valor do empréstimo, tempo em anos, 
        a data inicial e, opcionalmente, os juros.

        :param valor_emprestimo: Valor total do empréstimo.
        :param tempo_anos: Duração do empréstimo em anos.
        :param data_inicial_str: Data inicial do empréstimo no formato 
        'dd/mm/yyyy'.
        :param taxa_juros: Taxa de juros anual. Se não fornecida, assume-se que
        não haverá juros sobre o empréstimo.
        """
        self.formato = '%d/%m/%Y'
        self.data_inicial_datetime = self._validar_data_inicial(data_inicial_str)
        self.valor_emprestimo = valor_emprestimo
        self.tempo_anos = tempo_anos
        self.taxa_juros = taxa_juros

        if self.taxa_juros:
            self._calcula_valor_juros()
            
    def _validar_data_inicial(self, data_str: str) -> datetime:
        """
        Valida e converte a data inicial de string para objeto datetime.

        :param data_str: Data inicial como string.
        :return: Data inicial como objeto datetime.
        :raises ValueError: Se a data estiver no formato incorreto.
        """
        try:
            data = datetime.strptime(data_str, self.formato)
            return data
        except ValueError:
            raise ValueError(f'Data inicial "{data_str}" não está no\
 formato correto "dd/mm/aaaa"')
        
    @property
    def parcelas(self) -> int:
        """
        Calcula o número total de parcelas.

        :return: Número total de parcelas.
        """
        return self.tempo_anos * 12
    
    @property
    def valor_parcela(self) -> float:
        """
        Calcula o valor de cada parcela.

        :return: Valor de cada parcela.
        """
        return self.valor_emprestimo/self.parcelas
  
    def _calcula_valor_juros(self) -> None: 
        """
        Calcula o valor do empréstimo com juros compostos.
        """
        # Fórmula: M = C * (1 + i)^t
        taxa = (1 + self.taxa_juros) ** self.tempo_anos
        self.valor_emprestimo *= taxa

    def _calcula_data_parcela_inicial(self) -> datetime:
        """
        Calcula a data da primeira parcela, baseada na data inicial.
        """
        delta_mes = relativedelta(months=1)
        return self.data_inicial_datetime + delta_mes
    
    def _formatar_parcela(self, data_parcela: datetime,
                        valor_parcela: float,
                        num_parcela: int
    ) -> str:
        """
        Formata uma parcela com sua data de vencimento, valor e número.
        """
        data_str = data_parcela.strftime(self.formato)
        valor_str = f'Valor: {round(valor_parcela, 2)}'
        contagem_parcelas = f'{num_parcela}/{self.parcelas}'
        return f'{data_str} {valor_str} {contagem_parcelas}'

    def imprime_parcelas_vencimentos(self) -> None:
        """
        Imprime o valor de cada parcela e a data de vencimento
        """
        lista_parcelas = self.calcula_parcelas_vencimentos()

        for parcela in lista_parcelas:
            print(parcela) 

    def calcula_parcelas_vencimentos(self) -> list[str]:
        """
        Calcula o prazo de pagamento de cada parcela.
        """
        data_parcela_atual = self._calcula_data_parcela_inicial()
        valor_parcela_atual = self.valor_parcela

        lista_parcelas = []
        
        for num_parcela in range(1, self.parcelas + 1):
            parcela_formatada = self._formatar_parcela(data_parcela_atual, valor_parcela_atual, num_parcela)
            lista_parcelas.append(parcela_formatada)
            data_parcela_atual += relativedelta(months=1)

        return lista_parcelas
    
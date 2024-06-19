from datetime import datetime
from dateutil.relativedelta import relativedelta


class Emprestimo:
    def __init__(self,
                valor_emprestimo: float,
                tempo_anos: int,
                data_inicial_str: str,
                taxa_juros: float | None = None
    ):
        """
        Inicializa a classe Emprestimo com o valor do empréstimo, tempo em anos, 
        a data inicial e, opcionalmente, os juros.

        :param valor_emprestimo: Valor total do empréstimo.
        :param tempo_anos: Duração do empréstimo em anos.
        :param data_inicial_str: Data inicial do empréstimo no formato 'dd/mm/yyyy'.
        :param taxa_juros: Taxa de juros anual.
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

        delta_mes = relativedelta(months=1)
        data_parcela_inicial = self.data_inicial_datetime + delta_mes

        lista_parcelas = []
        
        for parcela in range(1, self.parcelas + 1):
            data_str = data_parcela_inicial.strftime(self.formato)
            valor_str = f'Valor: {self.valor_parcela:.2f}'
            contagem_parcelas = f'{parcela}/{self.parcelas}'
            data_valor_parcelas = f'{data_str} {valor_str} {contagem_parcelas}'
            lista_parcelas.append(data_valor_parcelas)
            data_parcela_inicial += delta_mes

        return lista_parcelas


if __name__ == '__main__':
    teste = Emprestimo(100000000, 1, '10/02/2004', taxa_juros=0.1)
    teste.imprime_parcelas_vencimentos()
    # teste.mostra_vencimentos_valores()
#interface genérica SQLExecutor
#o agente e as tools vão apenas importar SQLExecutor ou o executor especifico(DUckDBExecutor ou AthenaExecutor por ex para um futuro

from abc import ABC, abstractmethod
import pandas as pd 

class SQLExecutor(ABC):
    """Interface genérica para executores SQL."""

    @abstractmethod
    def run_query(self, query: str) -> pd.DataFrame:
        """Executa uma query SQL e retorna um DataFrame pandas."""
        pass
import unittest
from services.aws_client import list_files, S3_BUCKET

class TestS3Connection(unittest.TestCase):
    def test_list_files(self):
        """Testa se a função list_files retorna uma lista de arquivos do bucket S3
        e verifica se há pelo menos um arquivo Parquet.
        """
        files = list_files()
        
        # Verifica se retornou uma lista
        self.assertIsInstance(files, list, "A função list_files não retornou uma lista.")
        
        # Mostra os primeiros 5 arquivos para debug
        print(f"Arquivos no bucket {S3_BUCKET}: {files[:5]}")
        
        # Verifica se há pelo menos um arquivo no bucket
        self.assertGreater(len(files), 0, "O bucket está vazio.")
        
        # Verifica se existe pelo menos um arquivo Parquet
        parquet_files = [f for f in files if f.endswith(".parquet")]
        self.assertGreater(len(parquet_files), 0, "Não há arquivos Parquet no bucket.")

if __name__ == '__main__':
    unittest.main()

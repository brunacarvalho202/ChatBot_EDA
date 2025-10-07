# 🤖 Chatbot de Análise de Dados com LLM e Integração em Cloud

## 📘 Descrição / Objetivo

O foco deste projeto é o desenvolvimento de uma **inteligência artificial para análise exploratória de dados na nuvem**, utilizando **modelos de linguagem (LLMs)** para interpretar perguntas feitas em linguagem natural e traduzi-las em operações de análise sobre um dataset real.



### Principais objetivos do desafio:

1. **Criar um chatbot inteligente** que utilize um modelo de linguagem (LLM) para auxiliar usuários em tarefas de **análise exploratória de dados (EDA)**.  
2. Permitir que o usuário envie **consultas em linguagem natural**, e o chatbot seja capaz de interpretá-las corretamente.  
3. Fazer com que o chatbot **traduza essas consultas** em operações SQL/Pandas apropriadas sobre uma **base de dados hospedada em cloud**
4. Retornar **insights significativos e visualizações** a partir dos resultados obtidos, de forma clara e interativa.  




---
## 🏷️ Evidências, com prints e vídeo, de como o chatbot está reagindo até esse ponto da implementação:
---

LINK DO VIDEO DE DEMONSTRAÇÃO: [https://youtu.be/Z6yg7dRSofI?si=WbTZh6PVjBSFX0BC]  <br>


![WhatsApp Image 2025-10-06 at 12 55 35](https://github.com/user-attachments/assets/fda60630-1858-42fa-9c9e-27189b2a18bd)

![WhatsApp Image 2025-10-06 at 14 32 50](https://github.com/user-attachments/assets/f03371bd-b241-40e9-b2e7-888df49e65fc)

![WhatsApp Image 2025-10-06 at 14 35 18](https://github.com/user-attachments/assets/6095bc36-4ea0-4d74-9a64-19d6048bd55e)


## 📊 Observação sobre o Dataset usado

O dataset original contém cerca de **150 colunas**, relacionadas ao **contexto de concessão de crédito** e perfil financeiro de indivíduos.  
No entanto, para o escopo deste desafio, o chatbot foi projetado para trabalhar apenas com as seguintes colunas relevantes:

| Coluna     | Descrição                                                                 |
|-------------|---------------------------------------------------------------------------|
| `REF_DATE`  | Data de referência do registro                                            |
| `TARGET`    | Alvo binário de inadimplência (1 = Mau pagador, atraso > 60 dias em 2 meses) |
| `VAR2`      | Sexo do indivíduo                                                         |
| `IDADE`     | Idade do indivíduo                                                        |
| `VAR4`      | Flag de óbito (indica se o indivíduo faleceu)                             |
| `VAR5`      | Unidade Federativa (UF) brasileira                                        |
| `VAR8`      | Classe social estimada                                                    |

🔸 O dataset foi convertido do formato **CSV** para **Parquet**, visando maior eficiência de leitura e compressão.  
🔸 A versão final está **armazenada em um bucket S3 da AWS**, acessada diretamente pela aplicação.



---

## 🧩 Tecnologias utilizadas e seus motivos de escolha diante do cenário do desafio

- **Python 3.10+**
- **Streamlit** — Interface de chatbot e visualização (Simplicidade e rapidez para desenvolvimento)
- **LangChain** — Orquestração de ferramentas e raciocínio do LLM (Traz uma abstração da lógica complexa para ser implementada entre os componentes usados)
- **DuckDB** — Engine SQL local integrada à cloud (Aplica a query SQL diretamente no parquet que está armazenado na aws s3 e foi fortemente recomendado)
- **AWS S3 e boto3** — Armazenamento de dados em Parquet (Já tinha usado uma vez para estudo e foi mais familiar, considerando os créditos disponíveis e rapidez na implementação)
- **Pandas / Matplotlib / Seaborn / Plotly** — Manipulação e visualização de dados (Apesar de usar SQL, a entrada dos usuário pode ser melhor respondida em certos cenários com outras bibliotecas do python)
- **Google Vertex AI (ChatVertexAI)** — Modelos de linguagem (LLM) (O crédito liberado para uso foi maior em relação aos outros testados que tiveram problema no teste -openai e dois modelos do hugging face-)
- **Python-dotenv** — Carregamento de variáveis de ambiente (Por segurança guardar as credenciais dos serviços necessários na lógica)
- **LLM usado no Vertex: gemini-2.0-flash-001**


---


## 🧠 Arquitetura

Durante o desenvolvimento do desafio, foi usado um quadro no drawio onde registrei todo meu fluxo de pensamento e diagramas (percorrer ele pois é um mapa mental): [https://drive.google.com/file/d/11ktLvDx5ljq2JsvZM34S9gztqkTtwF0Y/view?usp=sharing]

<img width="8377" height="8822" alt="flow" src="https://github.com/user-attachments/assets/3927efc6-689a-47ea-99c6-236b6d3e2d1c" />


- **Frontend:** Chatbot interativo desenvolvido em **Streamlit**, capaz de receber perguntas em linguagem natural e exibir respostas em texto, tabelas e gráficos.  
- **Orquestração / Backend:** **LangChain** coordena as chains que transformam consultas do usuário em queries SQL, código Pandas e insights textuais.  
- **LLM:** **Google Vertex AI (ChatVertexAI)** interpreta as perguntas, gera queries e insights.  
- **Database Engine:** **DuckDB** executa consultas rápidas sobre os dados em formato Parquet, armazenados na nuvem.  
- **Cloud Storage:** **AWS S3** armazena os datasets em formato Parquet para acesso eficiente. (o csv tambem foi armazenado por )
- **Visualização e análise:** **Pandas**, **Matplotlib**, **Seaborn** e **Plotly** processam e exibem dados de forma interativa e estática.
  

---

## 🚧 Desafios enfrentados

- Dificuldades em lidar com credenciais em cloud (AWS, GCP, etc.)
- Problemas com os LLM (openai não tinha mais quota, dois modelos do hugging face não permitiam e etc)
- Problemas com as variáveis de ambiente (Tinha que ficar manipulando no terminal a declaração e verificação delas por que dava erro 403 entre tempos - precisava entender melhor o funcionamento do dotenv -)
- Estudo em pouco tempo das principais ferramentas usadas (LangChain e DuckDB -ainda não tinha usado essas ferramentas-)
- Em lidar com as ferramentas novas, junto com o prazo e querer melhorar o script de ETL aplicado (Precisei priorizar e planejar próximos passos constatemente a medida que dificuldades ou erros apareciam)
- Criação dos mocks para as classes de teste unitários e não ficar usando as chamadas reais do s3 e LLM

---

## 🔮 Próximas melhorias

- Mudar a abordagem sequencial para dinamica que usei com langchain (Percebi depois de estudar que usei uma forma sequencial do langchain com as chains e poderia ser mais dinamico com o aente decidindo a tool [])
- Melhorar a contextualização do LLM para evitar erros de interpretação  
- Adicionar suporte a gráficos (Não consegui fazer rodar ainda essa tool, está em análise -  as tools de gráfico existem e foram testadas mas não foram encaixadas no fluxo sequencial das chains)
- Implementar cache local de resultados
- Melhorar o script de limpeza e transformação nos dados (tem colunas que estão retornando com valores nulos quando não deveria, como idade por exemplo)
- Pesquisar uma forma mais otimizada de fazer as consultas (seja com outra tecnologia como Athena ou outra extensão diferente do parquet)
- Refatorar os testes unitários para ter uma melhor cobertura do projeto (ajustar os mocks e acrescentar testes unitários para cada tool)
- Aperfeiçoar os prompts e docs strings usadas para ter um melhor uso da LLM
- Analisar, debugar e refatorar a estrutura da chain para a orquestração ocorrer de uma melhor forma

---

---
## ⚙️ Como usar o projeto

**Resumo inicial:** as intruções são para rodar em localhost com o dockerfile disponivel, mas para rodar por completo esse projeto você precisa gerar suas credenciais pessoais dos serviços externos usados, como o llm e o aws s3. 

a documentação da langchain para uso dos modelos vertex que usei pode ajudar: [https://share.google/nRPyHueEGS6eqQUeI]

- **[PASSO 1]** Clonar o repositório:

comando: ```git clone https://github.com/brunacarvalho202/ChatBot_EDA.git```

- **[PASSO 2]** Criar suas credenciais para os serviços usados como os usados: aws s3 e modelo de llm gemini-2.0-flash-001 <br>
- **[PASSO 3]** Criar arquivos sensíveis que são usados mas não foram expostos como .env e config.py

  **observação 1: abaixo estão as variaveis de ambiente usadas para voce usar as mesmas se nao quiser adaptar seu projeto**


```env
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
S3_BUCKET=
S3_KEY=
S3_DATASET_PATH=
S3_PARQUET_PATH=
GOOGLE_APPLICATION_CREDENTIALS=
```


  **observação 2: abaixo um modelo do arquivo config.py para você usar se precisar**

```python
import os
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_KEY = os.getenv("S3_KEY")
S3_DATASET_PATH = os.getenv("S3_DATASET_PATH")
S3_PARQUET_PATH = os.getenv("S3_PARQUET_PATH")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
PROJECT_ID = "<SEU_PROJECT_ID_DO_GOOGLE>"
CREDENTIALS = GOOGLE_APPLICATION_CREDENTIALS
 ```


- **[PASSO 4]** Rodar o container Docker com o comando que está dentro dele (Substitua /caminho/local/ pelos caminhos corretos no seu computador)
- **[PASSO 5]** Acessar o chatbot localmente: **http://localhost:8501**


---

## 🧠 Pontos levados em consideração durante o desenvolvimento: 

**(Não estão em ordem de prioridade, apenas por organização)** <br>
**(Mesmo que tenham sido atendidos em uma certa porcentagem, são levados em consideração para as próximas refatorações**


**1. ESCALABILIDADE (decisões de design que permitam escalar o chatbot para conjuntos de dados maiores ou consultas mais complexas)** <br>
**2. EXTENSIBILIDADE: Estrutura clara que facilite a adição de novos recursos ou integração com outras fontes de dados**<br>


- O csv foi original foi armazenado na cloud para que caso haja necessidade de retornar a ele, já esta disponivel de ser acessado via serviços s3.
- O parquet foi gerado a partir do csv apenas com as colunas necessárias requisitadas para otimizar a consulta e já teve um script de limpeza e conversao de dados aplicado nele.
- O script de conversão csv -> parquet foi colocado na pasta de scripts para que caso queira mudar a lógica de ETL aplicada mexa apenas no script de ETL e/ou 
  caso precise gerar um novo parquet com outras especificações sejam feitas apenas adaptações como o nome do parquet que vai ser gerado
- O duckdb é apenas uma forma de aplicar a query, então caso venha ser refatorado para usar outra ferramenta, foi implementada um interface genérica que só precisa implementar o método de execute dela e passar a usar ele (além de não precisa apagar o do duckdb)
- Nas consultas, foi pensado para o SQL ser executado sempre primeiro mesmo que o escolhido de ser usado para que retorne apenas a oprção de dados que vai ser usada para as ferramentas posteriores


**3. INTERFACE DO CHATBOT: uma interface simples e intuitiva para interagir** <br>
**4. RESPOSTAS NATURAIS: deve responder em linguagem natural, explicando insihts de forma clara e concisa**<br>


- O chatbot foi pensado para ter a cara de chat comum onDe traz familiaridade e facilidade de uso. 
- Usa uma divisão entre a resposta do chat e a entrada do usuário apra as mensagens não fiquem perdidas.
- Tem apenas um campo de entrada e botão de enviar para atender ao objetivo principal dessa primeira versão
- os gráficos retornados tem pção de aumentar a visualização, pesquisar ou baixar ele
- O chatbot retorna um resumo textual do que foi mostrado em tabela


**5. ENTENDIMENTO DAS CONSULTAS: O chat deve interpretar corretamente consultas dos usuarios incluindo filtros, agregações e analise de tendencias** <br>
**6. PRECISÃO DAS RESPOSTAS: devem ser precisas e derivadas do conjunto de dados armazenado na cloud**<br>
**7. IMPLEMENTAÇÃO TÉCNICA: integração com LLM, integração com a Cloud, garantir consulas e recuperação de dados eficientes**<br>

- O fluxo conta com o uso de prompts estruturados para que cada vez mais as respostas sejam o padrão esperado e diminua os erros
- As consultas sql são instruídas a sempre virem com o caminho do arquivo do arquivo da cloud
- A escolha do langchain, além da abstração e facilidade, foi para ter um controle maior da orquestração das ferramentas a serem usadas na lógica, além da flexibilidade de refatorar esse fluxo


**8. QUALIDADE DO CÓDIGO: limpo, legivel, bem documentado**<br>
**9. TESTES: testes unitários para garantir a confiabilidade do código**<br>

- Pelo fato de a maioria das ferramentas terem sido o primeiro contato, o código ainda está com muito comentário para facilitar o estudo e documentação
- Os testes unitários visaram cobrir o máxima das configurações necessárias como conexões com os serviços




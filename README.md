# Case API com Flask

Este projeto é uma API desenvolvida com o framework **Flask**, usando várias bibliotecas para auxiliar em seu desenvolvimento, testes, e para persistência temporária de dados. A API foi projetada para ser leve e de fácil extensão, adequada para aplicações de pequeno a médio porte.

## Índice
- [Subir a APi no Docker](#rodar-com-docker-compose)
- [Endpoints](#endpoints)
- [Escolhas Técnicas](#escolhas-técnicas)
  - [Framework](#framework)
  - [Bibliotecas Principais](#bibliotecas-principais)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Testes](#testes)
- [Melhorias](#melhorias)

## Rodar com docker-compose
Na raiz do projeto execute o seguinte comando.

```bash
  docker compose up
```

### Acessar Swagger

[http://localhost:8000/docs](http://localhost:8000/docs)


## Endpoints

A API possui os seguintes endpoints:

- **`/model/load/`**: Responsável por carregar o modelo no formato `.pkl`.
  
- **`/model/classify/`**: Este endpoint recebe uma requisição JSON com os seguintes parâmetros:

  - **SepalLengthCm**: Comprimento da sépala em centímetros (Float).
  - **SepalWidthCm**: Largura da sépala em centímetros (Float).
  - **PetalLengthCm**: Comprimento da pétala em centímetros (Float).
  - **PetalWidthCm**: Largura da pétala em centímetros (Float).
  - **Retorno**: Este endpoint retorna a classificação da flor, que pode ser uma das três categorias:
    - Iris-setosa
    - Iris-versicolor
    - Iris-virginica
- ***`/model/history/`**: Retorna o histórico de classificações realizadas. *Melhoria
- ***`health`**: Retorna a saúde da api. *Melhoria

## Escolhas técnicas

### Framework
` - FlaskApi`

### Bibliotecas principais
- `fastapi` - Biblioteca utilizada para criar a API;
- `pytest` - Uma das principais bibliotecas para criar testes em python;
- `mongomock` - Biblioteca utilizada para persistir o histórico de inferencias na memoria
-  `joblib`: Usada para carregar modelos treinados salvos em arquivos `.pkl`, como também suporta a criação de processamento paralelo, o que pode ser explorado para otimizar o uso dos núcleos da CPU em projetos mais avançados.


Foi escolhido o Flask-API por ser leve e fácil de usar. Tenho bastante familiaridade com o Flask; em todos os meus projetos pessoais, uso o Flask para desenvolver a API, pois é excelente para criar projetos pequenos e médios de forma rápida, clara, otimizada e leve.

## Estrutura do Projeto

Abaixo está a estrutura do projeto para organização do código e arquivos:

```plaintext
docs/                   # Documentação do projeto
src/
├── core/               # Configurações centrais e utilitários principais para a aplicação
├── db/                 # Configuração e conexão com o banco de dados
├── routes/             # Definição dos endpoints e rotas da API
├── schemas/            # Definição dos modelos de dados, incluindo validações e serializações
├── services/           # Lógica de negócios e serviços auxiliares
└── main.py             # Ponto de entrada principal da aplicação
tests/                  # Testes unitários e de integração
├── unitários           # Testes das funcoes da camada Services
├── integração          # Testes de integração dos endpoints da API
.gitignore              # Arquivos e diretórios ignorados pelo Git
Dockerfile              # Definição de imagem Docker para a aplicação * (Melhoria)
README.md               # Documentação principal do projeto 
docker-compose.yml      # Arquivo para orquestração de containers Docker (Melhoria)
pytest.ini              # Configurações para execução do pytest
requirements.txt        # Bibliotecas e dependências do projeto
```

Construí essa estrutura de projeto seguindo as boas práticas de desenvolvimento para um projeto de machine learning. Separei o projeto em pastas e módulos específicos, cada um com sua responsabilidade bem definida. Assim, consigo facilitar a escalabilidade e a manutenção do projeto, além de tornar mais simples a realização de testes e a garantia da qualidade do código.

Por exemplo, eu poderia adicionar na camada services/ o pré-processamento de dados específicos para cada endpoint, antes de realizar uma inferência do modelo. Outra opção seria criar um novo módulo para gerenciar todo o desenvolvimento e testes da pipeline do projeto de machine learning antes de subir para produção. Essa abordagem ajuda a garantir que o código esteja devidamente testado e validado, minimizando o risco de problemas em ambiente de produção.

Uma melhoria a destacar é o uso do Docker e do Docker Compose para facilitar o versionamento do projeto em ambientes simulados antes de realizar o deploy em produção. Essa abordagem permite automatizar o fluxo de deploys em diferentes ambientes, como Desenvolvimento (para testar a aplicação em um ambiente simulado), STAGE (um ambiente que se aproxima mais do de produção) e PRODUÇÃO (o ambiente de produção real). Com o Docker, também podemos integrar facilmente práticas de CI/CD, o que otimiza o processo de entrega e garante que a aplicação esteja sempre em um estado funcional e testado antes de ser implantada.

Portanto, a estrutura inicial do projeto foi pensada levando em consideração esses pontos principais. Seguindo boas práticas de desenvolvimento, como clean code e arquitetura limpa, assim, conseguimos criar um ambiente organizado, escalável, fácl manutenção, testavel e fácil leitura.

## Testes

Nos testes, foquei em implementar uma cobertura > 90% do código. Para isso, utilizei bibliotecas de mocking (pytest) e dados simulados para validar o funcionamento dos métodos que envolvem a regra de negócios. Esses testes foram realizados como testes unitários, abrangendo tanto o "caminho feliz" quanto os "caminhos tristes" (forçando as exceções).

A segunda etapa realizei testes de integração, na qual simulei o funcionamento dos meus endpoints, tanto para entradas de dados válidas quanto para entradas inválidas. Essa abordagem garante que a API funcionasse corretamente em diferentes cenários e garante que as interações entre os componetes do sistema funcionasse corretamente.

# Melhorias

Melhorias que eu destacaria que faz sentido no meu entendimento seria:

- **Monitoramento e registro dos logs**: Implementei um endpoint(`/model/history`) de registro para as inferências, registrando todos os dados de entrada e as inferencias do modelo. Isso faz com que utilizamos metricas para avaliar a performace e precisão modelo ao longo do tempo, além de monitorar possíveis data drifts em relação aos dados de entrada. Pensando na AWS, poderíamos persistir os dados no DynamoDB, pois ele é leve e possui baixa latência. Poderíamos utilizar o SageMaker e/ou o CloudWatch para monitorar o desempenho dos modelos. Também poderíamos desenvolver um algoritmo que utiliza métricas estatísticas, empregando lotes de dados históricos de forma gradual para avaliar a precisão do modelo, assim como as mudanças nos dados de entrada ao longo do tempo.

- **Segurança** -  Implementacao de boas praticas de autorização e autenticação para ter acesso aos endpoints. Usando por exemplo, JWT token, Auth, etc... Validacao dos dados de entrada para evitar ataques de SQL Injection, por exemplo.

- **Gerenciamento de Modelos e Versionamento**: Implementaria boas práticas utilizando MLflow para ter uma gestão de versões de modelos mais rápida e precisa. Assim, seria possível atualizar ou reverter modelos em produção e facilitar o experimento de modelos. Realizaria testes A/B para analisar vários modelos e versões em produção.

- **Implementação de Pipeline Automatizada**: Utilizaria ferramentas de orquestração de workflows, como Apache Airflow, para gerenciar o fluxo de dados e o ciclo de vida dos modelos de machine learning. Isso facilitaria a automação de tarefas recorrentes, como coleta de dados, pré-processamento e inferência. Adicionaria monitoramento na pipeline para antecipar possíveis erros no fluxo, evitando prejuízos ao ambiente de produção.

- **Testes Automatizados e CI/CD**: Expandiria a cobertura de testes para incluir testes de carga, por exemplo. Implementaria boas práticas de entrega contínua e integração contínua para automatizar os testes, a construção e o deploy da aplicação. As etapas seriam divididas em três ambientes: DESENVOLVIMENTO, STAGE e PRODUÇÃO, garantindo deploys de qualidade e testáveis.

- **Escalabilidade**: Implementaria endpoints e métodos assíncronos (Async) para suportar um grande volume de requisições sem travar as chamadas feitas. Dessa forma, garantiria a capacidade de lidar com requisições em larga escala. Permintindo escalonamento vertical.
# Testes: Vaga de Engenheiro de Software

Este repositório tem como objetivo cumprir o teste técnico para a vaga de Engenheiro de Software, conforme documento [test.pdf](doc/test.pdf).

Este desafio é dividido em três etapas:

* [Questões](#questões)
* [Código](#código)
  * [Endpoints da API](#endpoints-da-api)
* [Extração de dados](#extração-de-dados)


## Questões

O inicio do documento supramencionado possui algumas questões, que foram respondidas em um documento a parte, [cujo link é este aqui](doc/answers.md).

## Código

A segunda etapa consiste em utilizar o Apache Spark para responder as perguntas da sessão Extração de dados.

Aqui, tentei aproveitar o ensejo para criar uma aplicação cujo objetivo é automatizar o processo de extração de dados das URLs e fornecê-los posteriormente via Redis, ao invés de um simples script que responda as questões levantadas no teste.

Todas as dependências desta aplicação estão no arquivo `requirements.txt`, na raiz do repositório. O processo de deploy e execução da aplicação foi dockerizada, portanto, recomenda-se fortemente o uso do comando `docker-compose up`, afim de evitar trabalho manual neste processo.

Obviamente, por ser uma aplicação feita em poucas horas e para fins de demonstração, ela não é _production ready_.

O escopo atendido aqui foi:

* Expor uma camada de API REST, com endpoints para:
  * Envio de novas URLs para processamento (HTTP ou FTP);
  * Consulta de estatísticas extraídas por meio de processamentos anteriores;
* Sempre que uma URL for enviada, o sistema irá:
  * Enviar a URL para processamento em background;
  * Responder o usuário com uma mensagem de sucesso;
* O processamento em background, por sua vez consiste em:
  * Verificar se aquele arquivo já foi processado anteriormente;
  * Caso sim, finaliza processamento;
  * Caso não, realiza download;
  * Após download, utiliza o Apache Spark para realizar extração dos dados relativos à sessão Extração de dados;
  * Salvar o resultado no Redis, agregando no mesmo resultados de processamentos anteriores, para que haja posterior consulta destas estatísticas via API.

### Endpoints da API

#### Enviar nova URL para processamento: 

* Verbo: POST 
* Path: /v1/files

**Requisição:**

```json
  {
    "url": "ftp://ita.ee.lbl.gov/traces/NASA_access_log_Jul95.gz"
  }
```

**Resposta:**

Identica à requisição

**Atenção:**

O cabeçalho `Content-Type` deverá está presente, e com o valor `application/json`.

#### Obter estatísticas de processamento

* Verbo: GET
* Path: /v1/stats

**Resposta**

```json
  {
    "top_5_urls": [],
    "qty_404_by_day": {},
    "total_bytes": 53656682848,
    "total_errors": 20112,
    "unique_hosts": 125720
  }
```

## Extração de dados

Consiste em responder as seguintes questões:

1. Número de hosts únicos.

|Julho|Agosto| Total|
|:---:|:----:|:----:|
|67016| 62860|129876|

2. O total de erros 404.

|Julho|Agosto|Total|
|:---:|:----:|:---:|
|10845| 10056|20901|

3. Os 5 URLs que mais causaram erro 404.

Infelizmente, não foi possível atender este requisito. Será implementado futuramente.

4. Quantidade de erros 404 por dia.

Infelizmente, não foi possível atender este requisito. Será implementado futuramente.

5. O total de bytes retornados.

|   Julho   |   Agosto  |   Total   |
|:---------:|:---------:|:---------:|
|38695973491|26828341424|65524314915|

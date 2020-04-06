> Qual o ​​objetivo ​​do​​ comando​​ `​cache` ​​​em ​​Spark?

É um comando através do qual podemos armazenar resultados intermediários de processamento em memória.

Sua principal necessidade advém do fato de que as operações em Apache Spark são _lazy evaluated_, ou seja, não são executadas imediatamente após serem solicitadas. Isto fará com que, se você tiver operações repetitivas ao longo do seu programa, ela seja executada diversas vezes quando você de fato precisar do dado, havendo assim perda de performance.

O `cache` permitirá que você armazene resultados intermediários destes processamentos em memória, podendo reaproveitá-los posteriormente para outras operações.

> O mesmo código implementado em Spark é normalmente mais rápido que a implementação equivalente em _MapReduce_. Por quê?

Enquanto que o MapReduce do Hadoop utiliza o disco para realizar operações de forma distribuída no HDFS, o Apacke Spark utiliza a memória RAM, tornando-o assim mais rápido que o Hadoop/MapReduce.

> Qual é a função do `SparkContext​`?

O `SparkContext` é a abstração da conexão com um cluster de Apache Spark e suas configurações, e é por meio dele que interagimos com este cluster.

Conforme documentação oficial, podemos usar o `SparkContext` para criar RDDs, acumuladores ou propagar variáveis ao longo de um cluster de Apache Spark.

> Explique com suas palavras o que é _Resilient​ ​Distributed​ ​Datasets​ (RDD)_.

RDD é uma abstração do Apache Spark que nos permite interagir com conjuntos de dados (_datasets_). 

O Apache Spark carrega estes dados em memória, distribuindo-os ao longo do cluster (_Distributed_), e utilizando mecanismos internos que garantem certa tolerância à falhas em algum nó do cluster (_Resilient_).

> `GroupByKey​` ​é menos eficiente que  `reduceByKey​` ​em grandes _dataset_. Por quê?

---

> Explique o que o código _Scala_ abaixo faz.

```scala
val textFile = sc.textFile("hdfs://...")

val counts = textFile.flatMap(line => line.split(" "))
  .map(word => (word, 1))
  .reduceByKey(_ + _)

counts.saveAsTextFile("hdfs://...")
```

A explicação resumida é que ele conta quantidade de ocorrências de cada palavra em um arquivo de texto, salvando o resultado em outro arquivo de texto.

A explicação passo a passo é:

1. Carrega um arquivo a partir do de um sistema de arquivos HDFS;
2. Transforma o conteúdo do arquivo em um _array_ por meio de uma combinação das funções `flatMap` e `split`;
3. O conteúdo de cada índice do array é transformado de _string_ para _tuple_, onde o primeiro índice desta _tuple_ é a palavra e o segundo é o numeral um, represetando uma ocorrência daquela palavra;
4. No resultado do passo 3 é feita uma redução (`reduceByKey`), que consistirá basicamente em somar todas as ocorrências unitárias de cada palavra, obtendo-se assim uma lista com quantas vezes cada uma delas aparece no texto;
5. Salva o resultado em um arquivo de texto em um HDFS.

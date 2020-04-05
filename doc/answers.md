> Qual o ​​objetivo ​​do​​ comando​​ `​cache` ​​​em ​​Spark?

> O mesmo código implementado em Spark é normalmente mais rápido que a implementação equivalente em _MapReduce_. Por quê?

> Qual é a função do `SparkContext​`?

> Explique com suas palavras o que é _Resilient​ ​Distributed​ ​Datasets​ (RDD)_.

> `GroupByKey​` ​é menos eficiente que  `reduceByKey​` ​em grandes _dataset_. Por quê?

> Explique o que o código _Scala_ abaixo faz.

```scala
val textFile = sc.textFile("hdfs://...")

val counts = textFile.flatMap(line => line.split(" "))
  .map(word => (word, 1))
  .reduceByKey(_ + _)

counts.saveAsTextFile("hdfs://...")
```

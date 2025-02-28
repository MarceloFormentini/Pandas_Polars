# Comparação entre Pandas X Polars
Comandos para utilizar o ambiente virtual, instalar libs necessárias e gerar o arquivo requirements.txt.
```
python3 -m venv venv
. venv\Scripts\activate
pip3 install pandas
pip3 install polars
pip3 install matplotlib
pip3 freeze > requirements.txt
```

📌 Passos do Projeto
- Gerar um conjunto de dados grande, com 1 milhão de registros.
- Executar operações e comparar desempenho usando time.time().
- Funcionalidades para Comparação
  - Escrita de CSV
  - Leitura de CSV
  - Filtragem de dados
  - Agregação (média, soma, contagem)
  - Ordenação
  - Junção (merge/join)
  - Transformações (criação de colunas)
  - Conversão para JSON/parquet
  - Escrita de dados

📌 Explicação

É gerado um dataset grande, com 1 milhão de linhas, na sequência executa algumas operações, cada operação é medido o tempo de execução com time.time().

📈 O que será comparado?
| Operação       | Pandas                | Polars                      |
|----------------|-----------------------|-----------------------------|
| Escrita CSV    | `to_csv()`            | `write_csv()`               |
| Leitura CSV    | `read_csv()`          | `read_csv()`                |
| Filtragem      | `df[df["categoria"] == "A"]` | `df.filter(pl.col("categoria") == "A")` |
| Agregação      | `groupby().agg()`     | `group_by().agg()`          |
| Ordenação      | `sort_values()`       | `sort()`                    |
| Junção (merge) | `merge()`             | `join()`                    |
| Transformação  | `assign()`            | `with_columns()`            |
| Conversão JSON | `to_json()`           | `write_json()`              |

## Benefícios dessa abordagem
 - Testamos diferentes operações usadas em ciência de dados e ETL.
 - Permitimos comparação de desempenho real entre Pandas vs Polars.
 - Podemos ajustar para diferentes volumes de dados e testar escalabilidade.

Os dados são gerados em um dicionário Python e posteriormente convertidos para Pandas DataFrame e Polars DataFrame.


## Execução dos Testes e Medição do Tempo
Para cada operação, usamos a função time.time() antes e depois da execução para medir o tempo gasto.

## Visualização dos Resultados
Após coletar os tempos de execução de cada operação para Pandas e Polars, os dados são plotados em um gráfico usando Matplotlib.

## Conclusão
O gráfico final permite visualizar qual framework é mais rápido em cada operação.
Geralmente, Polars tem melhor desempenho para grandes volumes de dados por ser otimizado para processamento paralelo e lazy evaluation.
Pandas é mais tradicional e amplamente utilizado, mas pode ser mais lento em algumas operações.
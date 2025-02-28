import os
import time
import pandas as pd
import polars as pl
import numpy as np
import matplotlib.pyplot as plt

def generate_data(rows: int):
	data = {
		"id": np.arange(rows),
		"value": np.random.rand(rows) * 100,
		"category": np.random.choice(["A", "B", "C", "D"], rows)
	}

	return pd.DataFrame(data), pl.DataFrame(data)

def get_file_paths():
	arq_path = os.path.dirname(os.path.abspath(__file__))

	arq_pandas = arq_path + "\data_pandas.csv"
	arq_polars = arq_path + "\data_polars.csv"

	return arq_pandas, arq_polars

def define_operations(arq_pandas, arq_polars):
	operations = [
		("Escrita",
			lambda df: df.to_csv(arq_pandas, index=False),
			lambda df: df.write_csv(arq_polars)),
		("Leitura",
			lambda df: pd.read_csv(arq_pandas),
			lambda df: pl.read_csv(arq_polars)),
		("Filtragem",
			lambda df: df[df["value"] > 50],
			lambda df: df.filter(pl.col("value") > 50)),
		("Agregação",
			lambda df: df.agg({"value": ["mean", "sum", "count"]}),
			lambda df: df.select([
				pl.col("value").mean().alias("mean"),
				pl.col("value").sum().alias("sum"),
				pl.col("value").count().alias("count")
			])),
		("Ordenação",
			lambda df: df.sort_values("value"),
			lambda df: df.sort("value")),
		("Junção",
			lambda df: df.merge(df, on="id"), 
			lambda df: df.join(df, on="id", how="inner")),
		("Transformação",
			lambda df: df.assign(new_col=df["value"] * 2), 
			lambda df: df.with_columns((pl.col("value") * 2).alias("new_col"))),
		("Conversão",
			lambda df: df.to_json(),
			lambda df: df.write_json())
	]

	return operations

def measure_operation_time(operation, df):
	start = time.time()
	operation(df) if callable(operation) else operation()
	return time.time() - start

def perform_operation(operations, df_pandas, df_polars):
	results = {"Operação": [], "Pandas": [], "Polars": []}

	for name, pandas_op, polars_op in operations:
		pandas_time = measure_operation_time(pandas_op, df_pandas)
		polars_time = measure_operation_time(polars_op, df_polars)

		results["Operação"].append(name)
		results["Pandas"].append(pandas_time)
		results["Polars"].append(polars_time)

	return results

def create_bar_chart(results):
	fig, ax = plt.subplots(figsize=(10, 6))
	index = np.arange(len(results["Operação"]))
	bar_width = 0.35

	ax.bar(index, results["Pandas"], bar_width, label="Pandas", color="blue")
	ax.bar(index + bar_width, results["Polars"], bar_width, label="Polars", color="red")

	ax.set_xlabel("Operações")
	ax.set_ylabel("Tempo (segundos)")
	ax.set_title("Comparação de Desempenho: Pandas x Polars")
	ax.set_xticks(index + bar_width / 2)
	ax.set_xticklabels(results["Operação"], rotation=0, ha="right")
	ax.legend()

	return fig, ax

def add_table(fig, ax, results):
	table_data = [[op, f"{p:.6f}", f"{po:.6f}"] for op, p, po in zip(results["Operação"], results["Pandas"], results["Polars"])]

	table = plt.table(
		cellText=table_data,
		colLabels=["Operação", "Pandas (s)", "Polars (s)"], 
		cellLoc="center",
		loc="bottom",
		bbox=[0, -0.6, 1, 0.4]
	)

	table.auto_set_font_size(False)
	table.set_fontsize(8)

	plt.subplots_adjust(left=0.2, bottom=0.3)
	plt.tight_layout()

def main():
	rows = 10**6
	df_pandas, df_polars = generate_data(rows)
	arq_pandas, arq_polars = get_file_paths()

	if os.path.exists(arq_pandas):
		os.remove(arq_pandas)
	if os.path.exists(arq_polars):
		os.remove(arq_polars)

	operations = define_operations(arq_pandas, arq_polars)
	results = perform_operation(operations, df_pandas, df_polars)
	fig, ax = create_bar_chart(results)
	add_table(fig, ax, results)
	plt.show()

if __name__ == "__main__":
	main()
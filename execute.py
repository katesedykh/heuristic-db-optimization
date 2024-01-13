import sqlparse
import psycopg2
import random
import math
from heuristics import GeneticAlgorithm, SimulatedAnnealing

class CustomQueryOptimizer:
    def __init__(self, algorithms):
        self.algorithms = algorithms

        self.connection = psycopg2.connect(
            dbname="algo_project",
            user="mks_user",
            password="123456789",
            host="localhost"
        )


    def optimize_query(self, sql_query):
        parsed_query = sqlparse.parse(sql_query)[0]
        plans = [algorithm.apply(str(parsed_query)) for algorithm in self.algorithms]
        
        # eval
        best_plan = self.select_best_plan(plans)

        return best_plan

    def select_best_plan(self, plans):
        return random.choice(plans) #placeholder

    def execute_query(self, plan):
        print("plan", plan)
        if isinstance(plan, list):
            # Translate the plan to a SQL query
            sql_query = create_sql_query(plan)
            print("sql_query", sql_query)
            with self.connection.cursor() as cursor:
                cursor.execute(sql_query)
                result = cursor.fetchall()
                return result
        else:
            return "Executed a non-SQL plan: " + str(plan)


def create_sql_query(plan):
    query = "SELECT * FROM table1"

    conditions = []

    for p in plan:
        if p == 'hash_join':
            query += " INNER JOIN table2 ON table1.id = table2.id"
        elif p == 'seq_scan':
            # Replace 'actual_column_name' with the actual column name in your schema
            conditions.append("table1.actual_column_name = 'some_value'")
        elif p == 'index_scan':
            # Add logic for index_scan with the correct column name
            conditions.append("table1.actual_indexed_column_name = 'some_value'")
        elif p == 'nested_loop':
            # Add logic for nested_loop with the correct column name
            conditions.append("table1.actual_nested_column_name = 'some_value'")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    return query


optimizer = CustomQueryOptimizer([
    GeneticAlgorithm(population_size=100, gene_pool=['index_scan', 'seq_scan', 'hash_join', 'nested_loop'], mutation_rate=0.01, max_generations=50),
    SimulatedAnnealing(initial_temp=10000, cooling_rate=0.03, gene_pool=['index_scan', 'seq_scan', 'hash_join', 'nested_loop'], min_temperature=1.0 )
])


optimized_plan = optimizer.optimize_query("SELECT * FROM table1 JOIN table2 ON table1.id = table2.id")
result = optimizer.execute_query(optimized_plan)
optimizer.connection.close()

print(result)


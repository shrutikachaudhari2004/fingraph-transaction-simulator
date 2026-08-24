from pyflink.datastream import StreamExecutionEnvironment

env = StreamExecutionEnvironment.get_execution_environment()

data = env.from_collection([
    "Transaction 1",
    "Transaction 2",
    "Transaction 3",
    "Transaction 4"
])

data.print()

env.execute("Fingraph Flink Test")
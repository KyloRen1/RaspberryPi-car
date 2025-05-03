from dora import Node
import pyarrow as pa

node = Node()

while True:
      dora_event = node.next(0.01)
      if dora_event is None:
            break
      if dora_event["type"] == "INPUT":
            message = dora_event["value"][0].as_py()
            print(
                  f"""I heard {message}"""
            )
            
# This is a sample Python script.
from flow_logic import flow_handler,flow_graph

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import time


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ctx = {}
    while True:
        in_request = input("type your request: ")
        st_time = time.time()
        out_response, ctx = flow_handler.turn_handler(in_request, ctx, flow_graph.actor)
        print(f"{in_request:} -> {out_response}")
        total_time = time.time() - st_time
        print(f"exec time = {total_time:.3f}s")

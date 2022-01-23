import logging
from typing import Union, Optional

from df_engine.core import Actor, Context
from flow_logic import flow_graph


class FlowHandler:
    def __init__(self, graph: flow_graph.FlowGraph ,logger: logging.Logger):
        self.logger = logger
        self.graph = graph
        self.actor = Actor(plot=self.graph.plot, start_label=("global", "start"))

    def turn_handler(self,
            in_request: str, ctx: Union[Context, str, dict], true_out_response: Optional[str] = None
    ):
        # Context.cast - gets an object type of [Context, str, dict] returns an object type of Context
        ctx = Context.cast(ctx)
        # Add in current context a next request of user
        ctx.add_request(in_request)
        # pass the context into actor and it returns updated context with actor response
        ctx = self.actor(ctx)
        # get last actor response from the context
        out_response = ctx.last_response
        # the next condition branching needs for testing
        if true_out_response is not None and true_out_response != out_response:
            msg = f"in_request={in_request} -> true_out_response != out_response: {true_out_response} != {out_response}"
            raise Exception(msg)
        else:
            self.logger.info(f"in_request={in_request} -> {out_response}")
        return out_response, ctx

"""
def turn_handler(
                 in_request: str, ctx: Union[Context, str, dict], actor: Actor, true_out_response: Optional[str] = None
                 ):
    # Context.cast - gets an object type of [Context, str, dict] returns an object type of Context
    ctx = Context.cast(ctx)
    # Add in current context a next request of user
    ctx.add_request(in_request)
    # pass the context into actor and it returns updated context with actor response
    ctx = actor(ctx)
    # get last actor response from the context
    out_response = ctx.last_response
    # the next condition branching needs for testing
    if true_out_response is not None and true_out_response != out_response:
        msg = f"in_request={in_request} -> true_out_response != out_response: {true_out_response} != {out_response}"
        raise Exception(msg)
    else:
        logging.info(f"in_request={in_request} -> {out_response}")
    return out_response, ctx
"""


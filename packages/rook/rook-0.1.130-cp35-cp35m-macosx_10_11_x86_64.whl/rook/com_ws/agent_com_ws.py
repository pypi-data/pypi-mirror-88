import os
from rook.com_ws.singlethread.agent_com_ws import AgentCom as AgentComSingle
from rook.com_ws.multithread.agent_com_ws import AgentCom as AgentComMT
from rook.logger import logger

if os.getenv("ROOKOUT_SINGLETHREAD_COMM", "0") == "1":
    logger.info("Using single-threaded communication")
    AgentCom = AgentComSingle

else:
    logger.debug("Using multi-threaded communication")
    AgentCom = AgentComMT

import os
from src import model

class Logger:
    '''
    log clients
    '''
    directory = "logs/client_logs"

    def __init__(self):
        self.is_setup = False # if the logger is setup (first run is setup)
    
    def setup(self, agent : model.Agent) -> None:
        if not self.is_setup:
            self.is_setup = True

            self.path = f"{Logger.directory}/{agent.id}.log"

            # create directory if it doesn't exist
            try:
                os.mkdir(self.directory)
            except:
                pass

            # create log file
            with open(self.path, "w") as f:
                 pass
            
            # log first run
            self.info(f"{agent.id} is {['thief', 'police'][agent.agent_type]}")
    

    def log(self, message : str) -> None:
        if self.is_setup:
            with open(self.path, "a") as f:
                f.write(message + "\n")
        else:
            raise Exception("Logger not setup")
    
    def info(self, message : str) -> None:
        self.log(f"[INFO] : {message}")

    def error(self, message : str) -> None:
        self.log(f"[ERROR] : {message}")

            
        
    



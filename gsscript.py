class gsscript: 
#the first version, not support loop


    def __init__(self,text):
          
      state      = text.strip()
      self.state = ''
      
      if state.find("*")==0:
            self.type  = "note"
            self.state = state
            return

      if state.find("'")==0:
            self.type  = "grads"
            texls  = state.split("'")
            self.state = texls[1]
      else:
            self.type  = "gs"
            self.state = state
      
  






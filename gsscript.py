class gsscript: 
# Class to execute gs script in Python 3, first version, NOT SUPPORT LOOP CURRENTLY!!!
# As GS script file is input, two attributes will be returned:
# self.ga: a Grads enverionment, obtained by py3grad, please refer to https://github.com/meridionaljet/py3grads
# self.note: note in gs script
# Example for Python 3.6 : 
# from gsscript import gsscript
# gs   = gsscript("./gsscript.gs")
# print( gs.notes )
# vara = gs.ga.exp("vara")

   def __init__(self,gsfile):

     def gsstate(text):     
        'Function to identify the type and statement of GS script line'
        
        state      = text.strip()
        
        if   state.find("*") == 0:       # notes
              gsline_type  = "note"
              gsline_state = state + "\n"
        elif state.find("'") == 0:       # Grads command
              gsline_type  = "grads"
              texls  = state.split("'")
              gsline_state = texls[1]
        else:                            #GS command
              gsline_type  = "gs"
              gsline_state = state

        return [gsline_type, gsline_state]

     from py3grads import Grads
     ga    = Grads(verbose=False)
     notes = ""
     #execute GS script line by line
     gsdic = {
           "note"   : "notes = notes  +  gsline_state", # Record notes
           "grads"  : "ga(gsline_state)",               # Extract Grads command
           "gs"     : "gsline_state"                    # Execute GS command
     }
 
     for line in open(gsfile):
           if not line:
             continue
           if line == "return":
             break
           gsline_type, gsline_state = gsstate(line)
           exec(gsdic[gsline_type])

     self.ga = ga
     self.note = notes
 

from tkinter.messagebox import showerror


def safe_execute(func, msg=None):
    try:
        res = func()
        
        return res
    
    except Exception as e:
        showerror(
            "Erro!",
            str(e) if msg is None else msg
        )
    
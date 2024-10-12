from tkinter.messagebox import showerror


def safe_execute(func):
    try:
        res = func()
        
    except Exception as e:
        showerror(
            "Erro!",
            str(e)
        )
    
    return res
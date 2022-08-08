from fastapi import  HTTPException

def HttpResponse(status: bool, message: None, **info: None): 
    if status == False: 
        raise HTTPException(status_code=500, detail={"success": status,  "error":message })
    return {"success": status, "data":message, "info":info }
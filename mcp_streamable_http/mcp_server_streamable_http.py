import math
from fastmcp import FastMCP

mcp = FastMCP("serverStreamableHttp")
@mcp.tool()
def get_user_by_id(user_id:str)-> str:
    """Ottieni uno user in base al sui id"""
    if user_id == "123":
        return "Alessandro Capodanno"
    elif user_id == "456":
        return "Bob Marley"
    else:
        return "Utente sconosciuto"
@mcp.tool()
def get_user_by_email(email:str)-> str:
    """Ottieni uno user in base a una email"""
    if email == "acap@test.com":
        return "Alessandro Capodanno"
    elif email == "bob.marley@test.com":
        return "Bob Marley"
    else:
        return "Utente sconosciuto"
@mcp.tool()
def is_prime(n:int)->bool:
    """Verifica se questo numero e´ primo """
    if n < 2 :
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True
if __name__ == '__main__':
    mcp.run(transport="streamable-http")

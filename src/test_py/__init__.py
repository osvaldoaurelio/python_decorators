# Decorators são uma forma elegante de modificar ou estender o comportamento de funções ou métodos sem alterar seu código original.
# Eles são implementados como funções que recebem outra função como argumento e retornam uma nova função com funcionalidades adicionais.
# O uso do caractere @ torna a aplicação do decorator mais simples e legível, sendo muito útil para adicionar recursos como logs, 
# validações, autenticação, controle de tempo de execução e tratamento de erros.
# o parametro func representa a função original que está sendo decorada.
# *args permite que a função aceite um número variável de argumentos posicionais, 
# enquanto **kwargs permite que a função aceite um número variável de argumentos nomeados (chave-valor).
# @wraps(func) é um decorator que preserva as informações da função original, como nome, docstring e outros atributos,
# garantindo que a função decorada se comporte de maneira semelhante à função original.
# wrapper é a função interna que envolve a função original, adicionando funcionalidades adicionais antes ou depois da execução da função original.

from atexit import register
from functools import wraps
from typing import Callable, TypedDict

register(lambda : print(f"\n{'='*50}\n\t...é só isso\n\t...não tem mais jeito\n\t...acabou\n\t...boa sorte 🎶\n{'='*50}"))

class UserType(TypedDict):
    name: str
    is_logged: bool

def authentication_required[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"\n🔓 Autenticando usuário...")
        if isinstance(args[0], dict) and not args[0].get("is_logged", False):
            raise PermissionError("🔒 Usuário não autenticado.")
        
        return func(*args, **kwargs)

    return wrapper

def rate_limit(max_calls: int = 3):
    def decorator[**P, R](func: Callable[P, R]) -> Callable[P, R]:
        calls: int = 0
        
        def _reset_limite() -> None:
            nonlocal calls
            calls = 0
            print("🆕 Limite de chamadas redefinido para zero.")

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            nonlocal calls
            if calls >= max_calls:
                raise PermissionError("💥 Limite de chamadas excedido.")
            
            calls += 1
            print(f"🔄️ Chamada atual: {calls}: Limite de chamadas: {max_calls}")

            return func(*args, **kwargs)
        
        wrapper.__setattr__("reset_limite", _reset_limite)

        return wrapper

    return decorator

def transaction_log(canal: str):
    def decorator[**P, R](func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            user_name = args[0]['name'] if isinstance(args[0], dict) else 'unknown'
            print(f"🖨️  [LOG - {canal}]: {user_name} iniciou uma transação.")

            return func(*args, **kwargs)
        
        return wrapper

    return decorator

@authentication_required
@rate_limit()
@transaction_log(canal="Internet Banking")
def send_money(usuario: UserType, valor: float, destino: str) -> None:
    print(f"✅ {usuario['name']} transferindo R${valor} para {destino}...\n")

def main() -> None:
    usuario_logado: UserType = {"name": "João", "is_logged": True}
    usuario_nao_logado: UserType = {"name": "Maria", "is_logged": False}

    try:
        send_money(usuario_logado, valor=100.0, destino="Maria")
        send_money({**usuario_logado, "name": "Malu"}, valor=150.0, destino="Carlos")
        send_money({**usuario_logado, "name": "Victor"}, valor=50.0, destino="Pedro")
        # send_money(usuario_logado, valor=50.0, destino="Maria")
        send_money.reset_limite()
        send_money(usuario_logado, valor=50.0, destino="Pedro")
        send_money(usuario_nao_logado, valor=200.0, destino="Carlos")
    except PermissionError as e:
        print(f"Erro: {e}")  

if __name__ == "__main__":
    main()

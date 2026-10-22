# Decorators são uma forma elegante de modificar ou estender o comportamento de funções ou métodos sem alterar seu código original.
# Eles são implementados como funções que recebem outra função como argumento e retornam uma nova função com funcionalidades adicionais.
# O uso do caractere @ torna a aplicação do decorator mais simples e legível, sendo muito útil para adicionar recursos como logs, 
# validações, autenticação, controle de tempo de execução e tratamento de erros.
# o parametro func representa a função original que está sendo decorada.
# *args permite que a função aceite um número variável de argumentos posicionais, 
# enquanto **kwargs permite que a função aceite um número variável de argumentos nomeados (chave-valor).
# @functools.wraps(func) é um decorator que preserva as informações da função original, como nome, docstring e outros atributos,
# garantindo que a função decorada se comporte de maneira semelhante à função original.
# wrapper é a função interna que envolve a função original, adicionando funcionalidades adicionais antes ou depois da execução da função original.

import functools

def authentication_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\nAutenticando usuário...")

        if not kwargs.get("logado", False) and not args[0].get("logado", False):
            raise PermissionError("Usuário não autenticado.")
        
        return func(*args, **kwargs)

    return wrapper

def rate_limit(max_calls = 3):
    def decorator(func):
        calls = 0

        
        def __reset_limite():
            nonlocal calls
            calls = 0
            print("-> Limite de chamadas redefinido para zero.")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal calls
            if calls >= max_calls:
                raise PermissionError("Limite de chamadas excedido.")
            
            calls += 1
            print(f"Chamada atual: {calls}: Limite de chamadas: {max_calls}")

            return func(*args, **kwargs)
        
        wrapper.reset_limite = __reset_limite

        return wrapper

    return decorator

def transaction_log(canal: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[LOG - {canal}]: Usuário {args[0]['nome']} iniciou uma transação.")

            return func(*args, **kwargs)
        
        return wrapper

    return decorator

usuario_logado = {"nome": "João", "logado": True}
usuario_nao_logado = {"nome": "Maria", "logado": False}

@authentication_required
@rate_limit()
@transaction_log(canal="Internet Banking")
def send_money(usuario: dict, valor: float, destino: str) -> None:
    print(f"Transferindo R${valor} para {destino}...\n")

def main() -> None:
    try:
        send_money(usuario_logado, valor=100.0, destino="Maria")
        send_money(usuario_logado, valor=150.0, destino="Carlos")
        send_money(usuario_logado, valor=50.0, destino="Pedro")
        send_money.reset_limite()
        send_money(usuario_logado, valor=50.0, destino="Pedro")
        send_money(usuario_nao_logado, valor=200.0, destino="Carlos")
    except PermissionError as e:
        print(f"Erro: {e}")  

if __name__ == "__main__":
    main()

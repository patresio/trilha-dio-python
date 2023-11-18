import textwrap


def menu():
    menu = """\n
    ================ OPÇÕES ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [cn]\tConta Nova
    [lc]\tListar Contas
    [nc]\tNovo Cliente
    [q]\tSair
    => 
    """
    return input(textwrap.dedent(menu))


def depositar(valor, saldo, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\t\tR$ {valor:.2f}\n"
        print(f"\n=== Depósito de R$ {valor:.2f} realizado com sucesso! ===")
        return saldo, extrato
    print("\n@@@ Operação falhou! O valor informado é inválido. @@@")


def sacar(*, valor, saldo, limite, extrato, numero_saques, limite_saques):
    if valor > saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif valor > limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif numero_saques >= limite_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print(f"\n=== Saque de R$ {valor:.2f} realizado com sucesso! ===")
        return saldo, extrato, numero_saques
    print("\n@@@ Operação falhou! O valor informado é inválido. @@@")


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if extrato is None else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ")
    if cliente := filtrar_cliente(cpf, clientes):
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return
    nome = input("Informe o nome do completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Informe o endereço (logradouro, nro - bairro - cidade/estado(sigla)): ")
    clientes.append({"nome": nome, "data_nascimento": data_nascimento,
                    "cpf": cpf, "endereco": endereco})
    print("=== Cliente cadastrado com sucesso! ===")


def filtrar_cliente(cpf, clientes):
    cliente_filtrados = [
        cliente for cliente in clientes if cliente["cpf"] == cpf]
    return cliente_filtrados[0] if cliente_filtrados else None


def criar_conta(agencia, numero_conta, clientes):
    cpf = input("Informe o CPF do cliente: ")
    if cliente := filtrar_cliente(cpf, clientes):
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "cliente": cliente}
    print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['cliente']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    saldo = 0.0
    limite = 500.0
    extrato = ""
    numero_saques = 0
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(valor, saldo, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nc":
            criar_cliente(clientes)

        elif opcao == "cn":
            numero_conta = len(contas) + 1
            if conta := criar_conta(AGENCIA, numero_conta, clientes):
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()

# language: pt
Funcionalidade: Transferir dinheiro
Cenário:  Conta existe e valor da transferência < saldo ?  Não
	Dado que usuario selecionou transferir dinheiro no menu
	Quando if (Conta existe e valor da transferência < saldo ?) then (Não)
	Então Exibir transação inválida

Cenário:  Sim
	Dado que usuario selecionou transferir dinheiro no menu
	Quando else (Sim)
	Então Debita valor do cliente e credita valor da transferência na conta do usuario
	E Exibe resumo da transação


class Templates:
    @staticmethod
    def welcome_message():
        return (
            "Olá! Seja bem-vindo ao seu assistente financeiro pessoal. "
            "Estou aqui para ajudá-lo a gerenciar suas finanças de forma simples."
        )

    @staticmethod
    def transaction_confirmation(transaction):
        return (
            f"Transação de R$ {transaction.value:.2f} registrada como {transaction.money_type}."
        )

    @staticmethod
    def daily_summary(user, transactions):
        total_spent = sum(t.value for t in transactions if t.money_type == 'spent')
        total_received = sum(t.value for t in transactions if t.money_type == 'received')
        message = (
            f"Olá {user.name}, aqui está o seu resumo diário:\n"
            f"- Total gasto: R$ {total_spent:.2f}\n"
            f"- Total recebido: R$ {total_received:.2f}\n"
            "Continue me enviando suas transações para manter seu registro financeiro atualizado."
        )
        return message

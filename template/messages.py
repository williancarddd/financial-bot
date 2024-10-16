def welcome_message():
    return (
        "👋 Olá! Seja bem-vindo ao seu assistente financeiro pessoal. "
        "Estou aqui para ajudá-lo a administrar suas finanças de forma simples e prática."
    )

def introduction_message():
    return (
        "📊 Como funciona o nosso bot:\n"
        "1️⃣ Me envie mensagens com suas transações financeiras. Exemplo: 'Gastei R$ 50 com supermercado'.\n"
        "2️⃣ Eu irei registrar todas as suas transações e você pode consultar um resumo diário sempre que precisar!\n"
        "3️⃣ Use comandos como 'resumo diário' para ver o total de despesas e receitas.\n\n"
        "⚙️ Fique à vontade para enviar suas transações e vamos juntos organizar suas finanças! 💸"
    )

def transaction_confirmation(transaction):
    return (
        f"✅ Transação de R$ {transaction.value:.2f} registrada como {transaction.money_type}."
    )

def daily_summary(user, transactions):
    total_spent = sum(t.value for t in transactions if t.money_type == 'spent')
    total_received = sum(t.value for t in transactions if t.money_type == 'received')
    return (
        f"📅 Resumo Diário - {user.name}:\n"
        f"- Total gasto: R$ {total_spent:.2f}\n"
        f"- Total recebido: R$ {total_received:.2f}\n"
        "📈 Continue registrando suas transações para manter seu controle atualizado."
    )

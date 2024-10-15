# Use uma imagem base do Python
FROM python:3.9

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de requisitos
COPY requirements.txt .

# Instale as dependências
RUN pip install -r requirements.txt

# Copie o restante do código
COPY . .

# Exponha a porta da aplicação Flask
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "app.py"]

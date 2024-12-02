
# Como Configurar e Executar o Projeto

## 1. Clonar o Repositório

## 2. Configurar o Ambiente Virtual

### Windows
1. Criar o ambiente virtual:
   ```bash
   python -m venv venv
   ```
2. Ativar o ambiente virtual:
   ```bash
   .\venv\Scripts\activate
   ```

### Mac/Linux
1. Criar o ambiente virtual:
   ```bash
   python3 -m venv venv
   ```
2. Ativar o ambiente virtual:
   ```bash
   source venv/bin/activate
   ```

## 3. Instalar as Dependências
Com o ambiente virtual ativo:
```bash
pip install -r requirements.txt
```

## 4. Configurar a Base de Dados
1. Fazer as migrações:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## 5. Executar o Servidor
Inicia o servidor no endereço `0.0.0.0:8000`:
```bash
python manage.py runserver 0.0.0.0:8000
```

O projeto estará disponível no navegador em `http://0.0.0.0:8000`.

**Nota:** Para que outras máquinas acedam ao servidor, utilize o IP da máquina onde o servidor está a correr em vez de `0.0.0.0`. Certifique-se de que todas as máquinas estão conectadas à mesma rede.

## 6. Rotas do Servidor
- `/` - Página inicial.
- `/lobby` - Tela compartilhada.
- `/finish_game` - Terminar o jogo.

**Nota:** Caso ocorra algum erro durante o uso do servidor, acede à rota `/finish_game` para reiniciar e tentar novamente.

## 7. Iniciar servidor depois da instalação
   ```bash
   cd .\ScapeRoom\
   ```
 ```bash
   .\venv\Scripts\activate
   ```
 ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
## 8. Aceder ao Servidor
### Na própria máquina
`http://localhost:8000`
### Noutras máquinas
`http://IP_DA_MAQUINA:8000`






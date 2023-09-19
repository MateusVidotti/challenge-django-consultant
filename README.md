# Challenge Django Consultant
## _Teste Técnico para Consultor Django DigitalSys_

### Para executar
- Necessário o docker no ambiente
- Clone o diretório
- Acesse o diretório e execute`docker-compose up --build`
- URL admin do django: http://localhost:8000/admin (user: admin, password: admin)
- URL app web: http://localhost:8080/
- No arquivo `.env` estão as variáveis de ambiente

### Serviços utilizados
- banco de dados: PostgreSQL
- mensager broker: rabbitmq
- servidor web: httpd
- backend: django
- filas: celery
- api: DjangoRestFramework

### Sobre a solução desenvolvida
Para cumprir o desafio foram utilizados apenas dois models no django. Um para armazenar as solicitações de 
empréstimos e um para armazenar os campos extras do usuário. O formulário ficou com alguns campos fixo e com a
possibilidade de adição dos campos extras por meio da interface admin do django. A api ficou apenas com dois pontos
(root e loanrequest). Em loanrequest no método GET entrega para frontend os campos do formulário e no POST recebe os 
dados do formulário. Quando o sistema recebe uma nova solictação de empréstimo dispara uma tarefa celery solicitando 
a avaliação por meio da api da DigitalSys. Caso a proposta não seja aprovada pela api, será enviado um email informando.
Caso aprovada o admin/usuário do sistema será notificado que existe nova proposta para avaliação. Uma vez ocorrendo a 
avalição do admin/usuário, será enviado um email para o solicitante.

# Kubernetes, Estudo de Caso
Esta é uma versão demo, apenas para teste, de um programa chamado Lista de Tarefas, construído na núvem, no **Google Cloud Services**, sobre o framework do **Kubernetes**
e integrado ao **PostgreSQL** também em núvem utilizando o módulo de SQL do GCS.

## App: Lista de Tarefas
O app é uma simples lista de tarefas, com as funcionalidades de adicionar, excluir e editar tarefas. Escrito em **Python**, **HTML**, **CSS** e **Postgres**.

<p align="center">
  <img src="https://user-images.githubusercontent.com/68448759/135730727-e8dee513-061d-4221-a366-21cc525eed38.PNG" />
</p>

### Acesso
O App está disponível em cloud, rodando sobre a estrutura do Google Cloud Services e pode ser acessado via: https://34.83.178.158
O mesmo salva e acessa os dados da lista utilizando uma instância PostgreSQL também hospedada no GCS.

## Arquitetura
Uma Docker container image foi criada a partir [deste repositório](https://hub.docker.com/repository/docker/aguilerajoao/lista-de-tarefas).
A partir desta imagem faço o deploy com kubernetes utilizando sua ferramenta para command-line kubectl utilizando os seguintes comandos:

`kubectl apply -n lista-de-tarefas -f kubernetes/secrets/secret.yaml # crio as variaveis de sistema ex.: DB_PASS`

`kubectl apply -n lista-de-tarefas -f kubernetes/services/service.yaml # Resposavel por balancear o tráfego externo entre os pods`

`kubectl apply -f .\kubernetes\deployments\deployment.yaml # executa o deploy`

`kubectl apply -n lista-de-tarefas -f kubernetes/autoscale/autoscale.yaml # gera novas replicas do app caso nescessário`

---------

<p align="center">
  <img src="https://user-images.githubusercontent.com/68448759/134965244-d70df5ea-03e4-4a19-81e6-d6e6ccbcfe34.png" />
</p>



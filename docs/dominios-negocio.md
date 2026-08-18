# Domínios de Negócio – SOS Animais Matão

## 1. Introdução

O sistema SOS Animais Matão é uma aplicação web destinada ao registro e acompanhamento de denúncias de maus-tratos contra animais no município de Matão.

A partir das funcionalidades previstas para o sistema, foram identificados os principais domínios de negócio e seus respectivos atributos.

---

## 2. Domínio: Usuário

O domínio Usuário representa a pessoa que utiliza a plataforma para realizar seu cadastro, autenticar-se no sistema e registrar denúncias.

### Atributos

| Atributo     | Tipo     | Descrição                                      |
| ------------ | -------- | ---------------------------------------------- |
| id           | String   | Identificador único do usuário                 |
| nome         | String   | Nome completo do usuário                       |
| email        | String   | Endereço de e-mail utilizado para autenticação |
| senha        | String   | Credencial de acesso                           |
| telefone     | String   | Telefone para contato                          |
| dataCadastro | DateTime | Data em que o usuário foi cadastrado           |

---

## 3. Domínio: Denúncia

O domínio Denúncia representa o registro de uma ocorrência de possível maus-tratos contra animais.

### Atributos

| Atributo       | Tipo     | Descrição                                          |
| -------------- | -------- | -------------------------------------------------- |
| id             | String   | Identificador único da denúncia                    |
| titulo         | String   | Título ou identificação resumida da denúncia       |
| descricao      | String   | Descrição detalhada da ocorrência                  |
| dataHora       | DateTime | Data e horário do registro                         |
| status         | String   | Situação atual da denúncia                         |
| tipoMausTratos | String   | Tipo de maus-tratos relatado                       |
| usuarioId      | String   | Identificador do usuário responsável pelo registro |
| animalId       | String   | Identificador do animal relacionado                |
| localizacaoId  | String   | Identificador da localização da ocorrência         |

### Possíveis valores para status

* Registrada
* Em análise
* Em atendimento
* Resolvida
* Encerrada

---

## 4. Domínio: Animal

O domínio Animal representa o animal envolvido na ocorrência registrada na denúncia.

### Atributos

| Atributo    | Tipo    | Descrição                             |
| ----------- | ------- | ------------------------------------- |
| id          | String  | Identificador único do animal         |
| especie     | String  | Espécie do animal                     |
| raca        | String  | Raça do animal, quando conhecida      |
| quantidade  | Integer | Quantidade de animais envolvidos      |
| observacoes | String  | Informações adicionais sobre o animal |

---

## 5. Domínio: Localização

O domínio Localização representa o local onde ocorreu a situação denunciada.

### Atributos

| Atributo  | Tipo   | Descrição                          |
| --------- | ------ | ---------------------------------- |
| id        | String | Identificador único da localização |
| endereco  | String | Endereço ou descrição do local     |
| cidade    | String | Cidade da ocorrência               |
| estado    | String | Estado da ocorrência               |
| latitude  | Double | Coordenada geográfica de latitude  |
| longitude | Double | Coordenada geográfica de longitude |

Como o sistema possui funcionalidade de envio de localização geográfica, latitude e longitude são atributos importantes para identificar a posição do ocorrido.

---

## 6. Domínio: Evidência

O domínio Evidência representa os arquivos, principalmente fotografias, utilizados para comprovar ou complementar as informações da denúncia.

### Atributos

| Atributo    | Tipo     | Descrição                             |
| ----------- | -------- | ------------------------------------- |
| id          | String   | Identificador único da evidência      |
| urlFoto     | String   | Endereço do arquivo armazenado        |
| nomeArquivo | String   | Nome do arquivo enviado               |
| dataEnvio   | DateTime | Data e horário do envio               |
| denunciaId  | String   | Identificador da denúncia relacionada |

Uma denúncia pode possuir uma ou várias evidências.

---

## 7. Domínio: Acompanhamento da Denúncia

O domínio Acompanhamento da Denúncia representa as alterações realizadas durante o tratamento da ocorrência.

### Atributos

| Atributo        | Tipo     | Descrição                                  |
| --------------- | -------- | ------------------------------------------ |
| id              | String   | Identificador do acompanhamento            |
| denunciaId      | String   | Identificador da denúncia relacionada      |
| status          | String   | Novo status da denúncia                    |
| dataAtualizacao | DateTime | Data e horário da atualização              |
| observacao      | String   | Informações adicionais sobre a atualização |

---

## 8. Relacionamentos entre os domínios

Os principais relacionamentos identificados são:

* Um Usuário pode registrar várias Denúncias.
* Cada Denúncia pertence a um Usuário.
* Uma Denúncia está relacionada a um Animal.
* Uma Denúncia possui uma Localização.
* Uma Denúncia pode possuir várias Evidências.
* Uma Denúncia pode possuir vários registros de Acompanhamento.
* Cada Evidência pertence a uma Denúncia.
* Cada registro de Acompanhamento pertence a uma Denúncia.

### Representação simplificada

```text
USUÁRIO
   │
   │ 1:N
   ▼
DENÚNCIA
   │
   ├──────────► ANIMAL
   │
   ├──────────► LOCALIZAÇÃO
   │
   ├──────────► EVIDÊNCIA
   │                 N
   │
   └──────────► ACOMPANHAMENTO
                     N
```

---

## 9. Considerações finais

Os domínios identificados representam as principais informações necessárias para o funcionamento do SOS Animais Matão.

O domínio central é a Denúncia, pois concentra a ocorrência de maus-tratos e se relaciona com o usuário responsável pelo registro, o animal envolvido, a localização da ocorrência, as evidências fotográficas e o acompanhamento do atendimento.

Esses domínios podem servir como base para a implementação das estruturas de dados no Cloud Firestore e para a evolução do sistema.

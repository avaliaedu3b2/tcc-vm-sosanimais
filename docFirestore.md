<h1>Modelo de dados do Cloud Firestore</h1>
<p>O Cloud Firestore é um banco de dados NoSQL orientado a documentos, onde os dados são armazenados em documentos organizados em coleções, em vez de tabelas e linhas como em bancos SQL. Cada documento contém pares chave-valor e pode incluir dados simples ou estruturas mais complexas, como listas e objetos aninhados. Ele é otimizado para grandes volumes de documentos pequenos, e tanto coleções quanto documentos são criados automaticamente ao adicionar dados.</p>
<h1>Documentos</h1>
<p>EmCloud FirestoreA unidade de armazenamento é o documento. Um documento é um registro leve que contém campos, os quais correspondem a valores. Cada documento é identificado por um nome.</p>
<p>Um documento que representa um usuário alovelacepode ter a seguinte aparência:</p>
<img width="114" height="53" alt="Captura de tela 2026-04-22 172338" src="https://github.com/user-attachments/assets/2245412b-344d-4648-8942-ce4a5e0d2fda" />
<h2>Observação:</h2>
<p>O Cloud Firestore suporta vários tipos de dados, como booleanos, números, strings, localização geográfica, dados binários e timestamps. Além disso, permite estruturar informações usando arrays e objetos aninhados (mapas) dentro dos documentos.</p>
<p>Objetos complexos e aninhados em um documento são chamados de mapas. Por exemplo, você poderia estruturar o nome do usuário do exemplo acima com um mapa, assim:</p>
<img width="204" height="110" alt="image" src="https://github.com/user-attachments/assets/9044538d-c57c-49a7-9735-ca4f0de0308c" />
<p>Você pode notar que os documentos se parecem muito com JSON. Na verdade, eles são basicamente o mesmo formato. Existem algumas diferenças (por exemplo, os documentos suportam tipos de dados adicionais e são limitados pelo tamanho do documento ), mas, em geral, você pode tratá-los como registros JSON leves.</p>
<h1>Coleções</h1>
<p>Os documentos ficam armazenados em coleções, que são simplesmente contêineres para documentos. Por exemplo, você pode ter uma userscoleção para armazenar seus diversos usuários, cada um representado por um documento:</p>
<img width="242" height="220" alt="image" src="https://github.com/user-attachments/assets/00de0da1-20b9-47fc-92ea-5a4b6baf1c6e" />
<p>O Cloud Firestore é um banco de dados NoSQL orientado a documentos, onde os dados são armazenados em documentos organizados em coleções, em vez de tabelas e linhas como em bancos SQL. Cada documento contém pares chave-valor e pode incluir dados simples ou estruturas mais complexas, como listas e objetos aninhados. Ele é otimizado para grandes volumes de documentos pequenos, e tanto coleções quanto documentos são criados automaticamente ao adicionar dados.</p>
<h1>Referências</h1>
<p>Cada documento no Cloud Firestore é identificado pela sua localização no banco de dados. É possível criar referências para documentos ou coleções, que são objetos leves usados para apontar para esses locais. Essas referências podem ser criadas mesmo sem dados existentes e não geram operações de rede.
</p>
<h2>Observação:</h2>
<p>Referências de coleção e referências de documento são dois tipos distintos de referências e permitem realizar operações diferentes. Por exemplo, você pode usar uma referência de coleção para consultar os documentos da coleção e uma referência de documento para ler ou gravar um documento individual.</p>
<p>Para sua conveniência, você também pode criar referências especificando o caminho para um documento ou coleção como uma string, com os componentes do caminho separados por uma barra ( /). Por exemplo, para criar uma referência ao alovelacedocumento:</p>
<h1>Dados Hierárquicos</h1>
<p>Para entender como funcionam as estruturas de dados hierárquicas emCloud FirestoreConsidere, por exemplo, um aplicativo de bate-papo com mensagens e salas de bate-papo.
<p>Para entender como funcionam as estruturas de dados hierárquicas emCloud FirestoreConsidere, por exemplo, um aplicativo de bate-papo com mensagens e salas de bate-papo.

Você pode criar uma coleção chamada roomspara armazenar diferentes salas de bate-papo:</p>
<img width="221" height="143" alt="image" src="https://github.com/user-attachments/assets/b6472476-4702-4396-944a-f12242377408" />
<p>Como documentos no Cloud Firestore devem ser leves, não é ideal armazenar muitas mensagens diretamente no documento de uma sala de bate-papo. Em vez disso, o recomendado é usar subcoleções dentro do documento da sala para armazenar as mensagens.
</p>
<h1>Subcoleções</h1>
<p>A melhor maneira de armazenar mensagens nesse cenário é usando subcoleções. Uma subcoleção é uma coleção associada a um documento específico.</p>
<h2>Observação: </h2>
<p></p>ocê pode consultar subcoleções com o mesmo ID de coleção usando consultas de grupo de coleções .
<p>Você pode criar uma subcoleção messagespara cada documento de sala em sua roomscoleção:</p>
<img width="263" height="295" alt="image" src="https://github.com/user-attachments/assets/05348990-1cde-487f-a1dd-714b68ef7685" />
<p>No Cloud Firestore, dados seguem um padrão alternado entre coleções e documentos, sem permitir coleção dentro de coleção ou documento dentro de documento diretamente. Subcoleções permitem organizar dados de forma hierárquica, facilitando o acesso (como armazenar mensagens dentro de uma sala). Além disso, documentos podem ter subcoleções aninhadas em até 100 níveis de profundidade.
</p>
<h2>Atenção:</h2>
<p>No Cloud Firestore, ao excluir um documento, suas subcoleções não são removidas automaticamente. Para apagar os dados dentro dessas subcoleções, é necessário excluí-los manualmente.
</p>



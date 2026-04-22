<h1> Adicionar o SDK Admin do Firebase ao servidor<h1>
<p>O Admin SDK do Firebase é um conjunto de bibliotecas voltado para uso em servidores com privilégios elevados, permitindo gerenciar e acessar recursos do Firebase e do Google Cloud de forma completa. Com ele, é possível ler e gravar dados, executar operações em larga escala, enviar notificações, autenticar usuários e criar ferramentas administrativas. Em essência, ele é utilizado no backend para realizar ações seguras e com controle total, não sendo indicado para uso direto por usuários finais.</p>
<h1>Pré-requisitos</h1>
<p>Verifique se você possui um app de servidor e se ele atende aos requisitos mínimos do Admin SDK conforme a linguagem usada. Em geral, são exigidas versões recentes das plataformas (como Node.js, Java, Python, Go e .NET), sendo que versões mais antigas já tiveram suporte descontinuado.</p>
<h1>Configurar um projeto e uma conta de serviço do Firebase</h1>
<p>Para usar o Firebase Admin SDK, é necessário ter um projeto do Firebase, uma conta de serviço (gerada automaticamente ao criar o projeto) e um arquivo de credenciais para autenticação. Caso ainda não tenha um projeto, é preciso criá-lo no console do Firebase antes de começar.</p>
<h1>Adicionar o SDK</h1>
<p>Se você estiver configurando um novo projeto, será necessário instalar o SDK para a linguagem de sua escolha.</p>
<img width="603" height="56" alt="Captura de tela 2026-04-22 165535" src="https://github.com/user-attachments/assets/199dacba-8074-4101-842c-50f546e47d1f" />
<p>Ou, para instalar a biblioteca apenas para o usuário atual, passe a flag --user:</p>
<img width="604" height="58" alt="Captura de tela 2026-04-22 165547" src="https://github.com/user-attachments/assets/170cf3dd-2f07-47e2-8047-01305bc0fb80" />
<h1>Inicializar o SDK</h1>
<p>Após criar um projeto no Firebase, o SDK pode ser inicializado usando as credenciais padrão do Google, um método automatizado e recomendado para ambientes como Cloud Run, App Engine e Cloud Functions. Para configurar serviços específicos, é possível usar a variável de ambiente FIREBASE_CONFIG, que pode conter diretamente um JSON com as configurações ou o caminho para um arquivo JSON.</p>
<img width="599" height="51" alt="Captura de tela 2026-04-22 170818" src="https://github.com/user-attachments/assets/4ff41a2f-2b61-4eff-a27b-17c3fbd20070" />
<h1>Como usar um token de atualização do OAuth 2.0</h1>
<p>O Admin SDK também fornece uma credencial que permite a autenticação com um token de atualização do Google OAuth2:</p>
<img width="595" height="71" alt="Captura de tela 2026-04-22 170951" src="https://github.com/user-attachments/assets/1e20f2a1-8ef1-47b9-9a87-81095e43b2ba" />
<h1>Inicializar o SDK em ambientes que não são do Google</h1>
<p>Em ambientes de servidor fora do Google, o Firebase Admin SDK deve ser inicializado usando um arquivo de chave da conta de serviço. Essas chaves exigem alto cuidado de segurança, pois são sensíveis. Para utilizá-las, é necessário gerar um arquivo JSON no console do Firebase e armazená-lo com segurança. A autenticação pode ser feita definindo a variável de ambiente GOOGLE_APPLICATION_CREDENTIALS com o caminho do arquivo (opção mais recomendada) ou informando esse caminho diretamente no código.</p>
<img width="589" height="57" alt="Captura de tela 2026-04-22 171111" src="https://github.com/user-attachments/assets/137281c8-f290-46e9-ae21-33d48e641e84" />
<p>Depois de concluir as etapas acima, o Application Default Credentials (ADC) poderá determinar implicitamente suas credenciais, permitindo que você use as credenciais da conta de serviço ao testar ou executar em ambientes que não são do Google.
Inicialize o SDK como mostrado:</p>
<img width="594" height="55" alt="Captura de tela 2026-04-22 171205" src="https://github.com/user-attachments/assets/bbc40f5e-387c-4dc6-9fa6-d6aa62e81f5e" />
<h1>Inicializar vários aplicativos</h1>
<p>Na maioria dos casos, você só precisa inicializar um único aplicativo padrão. Você pode acessar serviços fora desse aplicativo de duas maneiras equivalentes:</p>
<img width="599" height="170" alt="Captura de tela 2026-04-22 171258" src="https://github.com/user-attachments/assets/ff317f63-b398-404f-8db0-f9094607e018" />
<p>Em alguns casos, é necessário usar vários aplicativos Firebase ao mesmo tempo, como acessar dados de um projeto e autenticar outro. O Firebase Admin SDK permite criar múltiplos apps simultaneamente, cada um com suas próprias configurações e credenciais.</p>
<img width="588" height="238" alt="Captura de tela 2026-04-22 171355" src="https://github.com/user-attachments/assets/976b0e9e-e274-4fba-9c8f-ee9cfc67d80d" />
<h1>Definir escopos para Realtime Database e Authentication</h1>
<p>Ao usar uma VM do Google Compute Engine com credenciais padrão para Realtime Database ou Authentication, é necessário configurar os escopos de acesso adequados, como userinfo.email e cloud-platform ou firebase.database, podendo verificá-los e ajustá-los com o gcloud.</p>
<img width="596" height="311" alt="Captura de tela 2026-04-22 171456" src="https://github.com/user-attachments/assets/d5f33b49-3b7a-45e5-a22e-edae04686491" />
<h1>Como testar com credenciais de usuário final da gcloud</h1>
<p>Ao testar o Admin SDK localmente com credenciais padrão geradas pelo gcloud, são necessários ajustes para usar o Firebase Authentication, pois ele não aceita credenciais de usuário final padrão e exige o ID do projeto na inicialização. Como alternativa, é possível gerar credenciais usando um ID de cliente OAuth 2.0 próprio, do tipo aplicativo para computador.</p>
<img width="593" height="57" alt="Captura de tela 2026-04-22 171602" src="https://github.com/user-attachments/assets/01bb9e69-e533-4609-b1ae-44733ad396e7" />
<p>É possível definir o ID do projeto diretamente na inicialização do aplicativo ou usar a variável de ambiente GOOGLE_CLOUD_PROJECT. Usar a variável é mais simples, pois dispensa outras configurações adicionais durante os testes.</p>
<img width="601" height="69" alt="Captura de tela 2026-04-22 171704" src="https://github.com/user-attachments/assets/db05b060-924a-4f58-bb1f-b6cab3c71eec" />
<h1>Próximas etapas</h1>
<p>Você pode aprender mais sobre o Firebase acessando aplicativos de exemplo, explorando o código-fonte no GitHub e lendo artigos sobre o Admin SDK. Além disso, é possível adicionar recursos ao seu aplicativo, como back-end com Cloud Functions, armazenamento de dados no Realtime Database ou Cloud Storage e envio de notificações com o Cloud Messaging.</p>

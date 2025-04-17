# Chatbot com banco vetorial e RAG destinado à utilização em área de Gestão Pública Corporativa.

## Introdução
Este projeto apresenta o desenvolvimento de um chatbot inteligente, baseado em arquitetura RAG (Retrieval-Augmented Generation), destinado a responder perguntas sobre o Decreto nº 11.246/2022. Utilizando técnicas de Processamento de Linguagem Natural, a aplicação visa tornar mais acessível a compreensão e a aplicação do referido decreto, especialmente em ambientes administrativos relacionados a licitações e gestão de contratos.
O decreto, que dispõe sobre a governança da Administração Pública Federal Direta, Autárquica e Fundacional, representa um marco na estruturação de processos decisórios fundamentados em evidências e orientações normativas claras. Nesse contexto, a ferramenta proposta contribui significativamente para a democratização do acesso às informações legais, promovendo maior transparência e agilidade na interpretação do texto normativo.

## Objetivo
A aplicação tem como principal objetivo viabilizar a consulta contextualizada ao Decreto nº 11.246/2022, a partir de perguntas formuladas em linguagem natural. O chatbot responde com base nos trechos originais do documento, priorizando a precisão, a clareza e a relevância das respostas, sem recorrer a informações externas ao texto oficial.
A principal contribuição para o ambiente laboral é a definição clara dos papeis relacionados à área da gestão corporativa, constituindo-se como ferramenta relevante para consultas rápidas e respostas contextualizadas, minimizando os efeitos negativos da imprecisão quanto às atribuições dos agentes públicos nos processos de planejamento e gestão de contratos.

## Metodologia
A aplicação foi desenvolvida especialmente com base nas bibliotecas LangChain, em comunicação com LLM da OpenIA (acessada vida token) e Streamlit, que fornece a interface interativa em ambiente web. O fluxo de processamento segue as seguintes etapas:

## Carregamento do Documento
O PDF contendo o decreto é carregado com o auxílio do PyPDFLoader e segmentado em blocos de texto utilizando o RecursiveCharacterTextSplitter. Essa abordagem permite o fracionamento semântico do conteúdo para facilitar a vetorização posterior.

## Geração de Embeddings e Armazenamento Vetorial
Os trechos do decreto são transformados em vetores semânticos por meio do modelo all-mpnet-base-v2 da biblioteca HuggingFace. Esses vetores são armazenados com persistência no banco vetorial ChromaDB, viabilizando consultas eficientes por similaridade.

## Arquitetura RAG com LLMs
Para responder às perguntas dos usuários, o sistema utiliza o modelo de linguagem GPT-4 da OpenAI. A resposta é gerada com base nos trechos mais relevantes do documento, previamente recuperados pela busca vetorial. Um template de prompt foi projetado para garantir que as respostas estejam ancoradas no conteúdo do decreto.

## Histórico de Conversa e Interatividade
A aplicação mantém o histórico da conversa durante a sessão, permitindo respostas mais coerentes ao longo da interação. O layout é organizado em blocos de mensagens, garantindo uma experiência fluida e acessível.

## Funcionamento
Ao abrir a aplicação, é convidado a inserir sua chave da OpenAI, armazenada em um arquivo .env (se pré configurado com o token, o usuário se depara diretamente com uma caixa para input de textos em linguagem natural, como no caso apresentação). Após a validação da chave, o chatbot torna-se funcional, oferecendo um campo de entrada para perguntas livres. Ao submeter uma dúvida, o sistema identifica os trechos mais relevantes do decreto, compõe um prompt personalizado e retorna uma resposta textual fundamentada.

A ferramenta demonstra especial utilidade em ambientes institucionais onde é necessária a consulta recorrente ao dispositivo normativo, oferecendo uma alternativa ágil e contextualizada ao texto completo.

## Resultados Esperados
Com a aplicação do chatbot, espera-se:

Agilidade nas consultas jurídicas, especialmente por parte de servidores públicos gestores, fiscais, comissões de contratação, equipes de apoio, etc. ;
Aprimoramento da governança institucional, pela facilidade de acesso a dispositivos legais atualizados;
Redução de erros interpretativos, ao basear as respostas exclusivamente nos trechos normativos;
Ampliação da cultura de dados e inteligência artificial na administração pública.

## Limitações e Considerações Finais
A precisão das respostas depende da qualidade dos embeddings gerados e da formulação das perguntas. Questões ambíguas ou excessivamente genéricas podem gerar respostas pouco úteis. Além disso, o modelo não retém memória entre sessões, o que limita interações contínuas de longo prazo.

Apesar dessas limitações, a aplicação cumpre satisfatoriamente seu propósito pedagógico e experimental, representando um avanço relevante no uso de inteligência artificial aplicada à consulta normativa.

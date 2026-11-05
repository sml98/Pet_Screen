# Instruções para agentes

Para criar ou adaptar um pet Android, leia e siga `skills/android-screen-pet/SKILL.md` e `docs/ADAPTAR-OUTRO-PACK.md`. Para pesquisar packs e gerar vários apps personalizados, leia também `docs/FABRICA-DE-APPS.md`.

- Entregue o APK quando esse for o pedido; preserve a prévia HTML offline e os arquivos fonte.
- O catálogo de personagens está em `app/src/main/assets/pets.json`. Use `tools/add_character.py` em vez de fixar contagens ou nomes no Java.
- Não trate dimensão do quadro como quadrada por padrão. Preserve alpha e proporção; mantenha Android e prévia equivalentes.
- O motor atual usa uma faixa horizontal por personagem e estados procedurais. Não alegue suporte a folhas por estado sem implementá-lo.
- Compile com o wrapper Gradle 8.9/JDK 17/SDK 35. Valide catálogo e prévia quando alterar assets ou comportamento.
- Não comite keystores, senhas, tokens, backups de assinatura, caminhos de SDK locais ou caches.
- A licença MIT cobre o código, não as artes fornecidas pelo usuário. Consulte `packs/ORIGEM-E-LICENCAS.md` antes de descrever direitos dos assets.
- Não publique ou mude acesso de repositórios fora da autorização do usuário. Uma autorização já dada na sessão continua válida.

# Verificação da versão 1.0

- APK release compilado com Android Gradle Plugin 8.7.3, Gradle 8.9, JDK 17 e Android SDK 35.
- `assembleRelease` e `lintRelease`: sucesso, zero erros e dez avisos de localização, compatibilidade e otimização. Relatório de assinatura em `verification/apk-signature.txt`.
- `apksigner verify`: assinatura APK v2 válida, RSA de 3072 bits, chave própria deste projeto.
- Manifesto verificado com aapt: minSdk 26 (Android 8), targetSdk 35 (Android 15); sem permissão INTERNET.
- Prévia verificada em Chromium com viewport móvel 390×844 e desktop 1280×1000: seis folhas de sprites, alimentação, carinho, dormir/acordar, arrasto, aterrissagem, personalização e persistência após recarregar. Zero erros JavaScript. Resultado em `verification/preview-test.json`; capturas em `preview/`.
- Validação das imagens: dimensões, número de quadros e limites alpha em `sprite-manifest.json`. A folha retangular da vassoura mantém 48×64 por quadro.

A compilação não substitui teste em cada modelo de celular. Nenhum aparelho físico foi utilizado. Fabricantes e apps podem impor restrições próprias ao overlay e à bateria. A prévia e o Android têm implementações separadas; testes da prévia não constituem testes do runtime Android.

## Runtime Android nesta sessão

Foi preparada uma imagem AOSP Android 15 em um emulador sem KVM. A inicialização excedeu oito minutos e não disponibilizou todos os serviços de pacote/janela. A tentativa de instalar foi recusada pelo próprio sistema por ausência do serviço `package`, antes da instalação do app. Portanto **a execução Android não foi validada neste ambiente**; nenhum resultado de sucesso foi atribuído ao teste `verification/android_smoke.py`. O APK continua com compilação, lint e assinatura verificados; a prévia tem testes próprios aprovados.

O script de smoke test pode ser executado em um emulador já inicializado ou aparelho dedicado com ADB; ele instala o APK, concede a permissão de overlay para o teste e interage com a tela. Use apenas um dispositivo de teste autorizado.

## Fluxo de variantes e ferramentas

O importador foi testado com uma grade 2×2 de quadros retangulares 48×64: ordem, dimensões, transparência e bloqueio de ID duplicado aprovados. `create_variant.py` gerou uma variante fictícia “Pet da Ana”, identificador `br.com.exemplo.petana`, personagem da vassoura e perfil Lua/fêmea/carinhosa/pastel. `assembleDebug` e `lintDebug` dessa variante passaram; o aapt confirmou o nome e identificador exclusivos. A prévia abriu com um único personagem e o perfil correto, sem erros JavaScript.

A busca de teste “dragon” retornou dois candidatos do OpenGameArt; isso valida a descoberta, não uma recomendação ou a licença desses assets. Nenhum pack adicional foi incorporado ao exemplo.

O workflow público também contém um job de smoke test Android 15 com KVM no GitHub Actions. Consulte o resultado da execução na aba Actions; a existência do job não significa, por si só, que passou.

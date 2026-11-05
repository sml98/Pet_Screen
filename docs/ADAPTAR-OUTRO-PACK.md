# Criar sua versão com outro pack

1. Faça um fork ou clone este repositório.
2. Baixe um pack cuja licença permita seu uso. Guarde a URL e o texto de licença do autor.
3. Abra a folha e descubra o tamanho real de cada quadro. Uma imagem de 288×64 pode conter seis quadros de 48×64: não corte automaticamente em quadrados.
4. Instale Python e `python -m pip install -r tools/requirements.txt`.
5. Importe a folha:

   ```bash
   python tools/add_character.py --sheet meu-pack/idle.png \
     --id meu-pet --name "Meu Pet" --frame-width 48 --frame-height 64 --fps 8
   python tools/validate_catalog.py
   python tools/rebuild_preview.py
   ```

6. Abra `preview/gato-de-tela.html` no navegador. Teste o personagem, arraste, alimente e faça carinho.
7. Para personalizar os gatos de 32×32 com os mesmos pontos de olhos e acessórios da base, importe com `--recolor --eyes --accessories`. Para outro desenho, adapte `Appearance.java`; essas coordenadas não são universais.
8. Escolha um `applicationId` próprio em `app/build.gradle` se quiser instalar sua versão junto com o exemplo. Edite o nome e ícone em `AndroidManifest.xml` e `res/drawable/`.
9. Compile com `./gradlew assembleDebug` ou use Actions → **Build Android APK** → **Run workflow** no seu fork. O resultado instalável fica nos artefatos da execução.
10. Para release, configure sua própria chave e os secrets descritos no README. Uma atualização precisa da mesma assinatura da instalação anterior.

O catálogo aceita faixas horizontais; o importador também aceita grades regulares e as normaliza sem esticar. Atlas irregulares precisam ser separados primeiro. A sequência é compartilhada pelos estados físicos da base. Para animações específicas de andar, dormir etc., um agente deve ampliar o motor para selecionar folhas por estado e manter a prévia equivalente.

O arquivo `packs/ScreenPet-Packs-Completo.zip` reúne os quatro packs enviados para este exemplo, os sprites ampliados e um índice pesquisável. Ele **não concede uma nova licença sobre as artes**: confira `packs/ORIGEM-E-LICENCAS.md`.

## Pedir a qualquer agente

Anexe seu pack e diga:

> Clone este repositório e siga `skills/android-screen-pet/SKILL.md`. Substitua ou acrescente meus personagens, mantenha os cuidados e a personalização e entregue o APK compilado, a prévia offline e os arquivos de origem. Não publique chaves de assinatura. Registre quais animações vieram do pack e quais foram adaptadas.

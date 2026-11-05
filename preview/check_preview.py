from playwright.sync_api import sync_playwright
from pathlib import Path
import json
r=Path(__file__).resolve().parent
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--no-sandbox']);page=browser.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto((r/'gato-de-tela.html').as_uri());page.wait_for_function('colored.length === 6');page.wait_for_timeout(500)
 page.locator('#name').fill('Luna');page.locator('#sex').select_option(label='Fêmea');page.locator('#personality').select_option(label='Carinhoso');page.locator('#fur').select_option(label='Lilás');page.locator('#eyes').select_option(label='Verde');page.locator('#outfit').select_option(label='Laço rosa');page.locator('#theme').select_option(label='Pastel');
 page.locator('#feed').click();assert float(page.locator('#food').get_attribute('value'))>99
 page.locator('#care').click();assert float(page.locator('#mood').get_attribute('value'))>95
 page.locator('#sleep').click();page.wait_for_timeout(200);assert 'Dormindo' in page.locator('#state').inner_text();page.locator('#sleep').click();
 for skin in ['Gato creme','Gato vampiro','Gato na caixa','Caixa Halloween','Bruxo na vassoura','Vampiro bravo']:
  page.locator('#skin').select_option(label=skin);page.wait_for_timeout(100)
 page.locator('#skin').select_option(label='Gato creme')
 # Real pointer events: move pet to the middle, release and observe landing.
 page.locator('#pet').scroll_into_view_if_needed();page.wait_for_timeout(100);box=page.locator('#pet').bounding_box();room=page.locator('#room').bounding_box();sx=box['x']+box['width']/2;sy=box['y']+box['height']/2
 page.mouse.move(sx,sy);page.mouse.down();page.mouse.move(room['x']+170,room['y']+110,steps=10);assert page.evaluate('drag.moved');page.mouse.up();page.wait_for_timeout(1300);assert page.evaluate('y>=room.clientHeight-Number($("size").value)-2')
 page.reload();page.wait_for_function('colored.length===6');assert page.locator('#name').input_value()=='Luna';assert page.locator('#sex').input_value()=='Fêmea';assert page.locator('#fur').input_value()=='Lilás';
 page.screenshot(path=str(r/'preview-mobile.png'),full_page=True)
 page.set_viewport_size({'width':1280,'height':1000});page.screenshot(path=str(r/'preview-desktop.png'),full_page=True)
 assert not errors,errors
 print(json.dumps({'result':'PASS','checks':['6 sprite sheets','feed','petting','sleep/wake','drag and landing','customization persistence','mobile and desktop rendering'],'browserErrors':errors},ensure_ascii=False))
 browser.close()

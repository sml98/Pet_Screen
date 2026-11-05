package com.catpack.pet;

import android.app.*;
import android.content.*;
import android.graphics.*;
import android.os.*;
import android.view.*;
import android.widget.*;

public class PetService extends Service {
 PetCatalog catalog; WindowManager wm; WindowManager.LayoutParams lp; PetView pet; LinearLayout panel; TextView meters;
 final Handler handler=new Handler(Looper.getMainLooper());
 boolean awake=true,registered=false,dragging=false,sleeping=false;
 float x,y,vx=65,vy,timer,clock,heart,food=85,energy=90,mood=80;
 int width,height,size,skin,fur,eyes,outfit,personality,sex,theme; String petName="Mingau"; String state="idle"; long last,lastNeeds,lastSave;
 float downX,downY,startX,startY; boolean moved;
 final Runnable loop=new Runnable(){public void run(){if(!awake||pet==null)return;long now=System.nanoTime();float dt=last==0?0:Math.min(.04f,(now-last)/1e9f);last=now;step(dt);handler.postDelayed(this,33);}};
 final BroadcastReceiver screen=new BroadcastReceiver(){public void onReceive(Context c,Intent i){awake=!Intent.ACTION_SCREEN_OFF.equals(i.getAction());handler.removeCallbacks(loop);last=0;if(awake){updateNeeds();handler.post(loop);}else{closePanel();save();}}};
 public IBinder onBind(Intent i){return null;}
 public void onCreate(){super.onCreate();ProfileDefaults.ensure(this);catalog=new PetCatalog(this);android.content.SharedPreferences p=getSharedPreferences("life",0);food=p.getFloat("food",85);energy=p.getFloat("energy",90);mood=p.getFloat("mood",80);sleeping=p.getBoolean("sleep",false);lastNeeds=p.getLong("time",System.currentTimeMillis());updateNeeds();}
 void updateNeeds(){long now=System.currentTimeMillis();float hours=Math.max(0,Math.min(24,(now-lastNeeds)/3600000f));food=clamp(food-hours*6);energy=clamp(energy+hours*(sleeping?28:personality==4?-12:-8));mood=clamp(mood-hours*3);lastNeeds=now;if(sleeping&&energy>=99){sleeping=false;enter("idle");}if(meters!=null)meters.setText(stats());}
 static float clamp(float n){return Math.max(0,Math.min(100,n));}
 void save(){getSharedPreferences("life",0).edit().putFloat("food",food).putFloat("energy",energy).putFloat("mood",mood).putBoolean("sleep",sleeping).putLong("time",lastNeeds).apply();lastSave=System.currentTimeMillis();}
 String stats(){return petName+" · "+(sex==0?"Macho":"Fêmea")+"\nSaciedade: "+Math.round(food)+"%\nEnergia: "+Math.round(energy)+"%\nHumor: "+Math.round(mood)+"%";}
 public int onStartCommand(Intent i,int flags,int id){
  if(i!=null&&"STOP".equals(i.getAction())){stopSelf();return START_NOT_STICKY;}
  if(!android.provider.Settings.canDrawOverlays(this)){stopSelf();return START_NOT_STICKY;}
  android.content.SharedPreferences cfg=getSharedPreferences("config",0);skin=catalog.safeIndex(cfg.getInt("skin",0));theme=cfg.getInt("theme",0);fur=cfg.getInt("fur",0);eyes=cfg.getInt("eyes",0);outfit=cfg.getInt("outfit",0);personality=cfg.getInt("personality",0);sex=cfg.getInt("sex",0);petName=cfg.getString("name","Mingau");
  NotificationManager nm=getSystemService(NotificationManager.class);nm.createNotificationChannel(new NotificationChannel("pet","Gato de Tela",NotificationManager.IMPORTANCE_LOW));
  PendingIntent stop=PendingIntent.getService(this,0,new Intent(this,PetService.class).setAction("STOP"),PendingIntent.FLAG_IMMUTABLE);
  PendingIntent open=PendingIntent.getActivity(this,1,new Intent(this,MainActivity.class),PendingIntent.FLAG_IMMUTABLE);
  Notification n=new Notification.Builder(this,"pet").setContentTitle(petName+" mora aqui 🐾").setContentText("Toque no gato para cuidar dele.").setSmallIcon(android.R.drawable.ic_menu_myplaces).setContentIntent(open).addAction(new Notification.Action.Builder(null,"Parar",stop).build()).setOngoing(true).build();
  if(Build.VERSION.SDK_INT>=34)startForeground(1,n,android.content.pm.ServiceInfo.FOREGROUND_SERVICE_TYPE_SPECIAL_USE);else startForeground(1,n);
  int wanted=(int)(Math.max(56,Math.min(160,cfg.getInt("size",88)))*getResources().getDisplayMetrics().density);
  if(pet!=null){size=wanted;lp.width=size;lp.height=size;pet.load();closePanel();return START_NOT_STICKY;}
  wm=getSystemService(WindowManager.class);size=wanted;bounds();x=width/2f;y=Math.max(0,height-size);pet=new PetView();
  lp=new WindowManager.LayoutParams(size,size,WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE|WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL,PixelFormat.TRANSLUCENT);lp.gravity=Gravity.TOP|Gravity.LEFT;lp.x=(int)x;lp.y=(int)y;
  try{wm.addView(pet,lp);}catch(RuntimeException e){pet=null;stopSelf();return START_NOT_STICKY;}
  IntentFilter filter=new IntentFilter();filter.addAction(Intent.ACTION_SCREEN_OFF);filter.addAction(Intent.ACTION_SCREEN_ON);
  if(Build.VERSION.SDK_INT>=33)registerReceiver(screen,filter,Context.RECEIVER_NOT_EXPORTED);else registerReceiver(screen,filter);registered=true;
  awake=getSystemService(PowerManager.class).isInteractive();if(awake)handler.post(loop);return START_NOT_STICKY;
 }
 void bounds(){android.util.DisplayMetrics m=new android.util.DisplayMetrics();wm.getDefaultDisplay().getMetrics(m);width=m.widthPixels;height=m.heightPixels;}
 void enter(String s){state=s;timer=0;}
 void step(float dt){bounds();clock+=dt;timer+=dt;heart=Math.max(0,heart-dt);updateNeeds();if(System.currentTimeMillis()-lastSave>30000)save();float right=Math.max(0,width-size),floor=Math.max(0,height-size);
  if(!dragging&&panel==null){
   if(sleeping){y=Math.min(floor,y+100*dt);state="sleep";}
   else switch(state){
    case "sleep":enter("fall");break;
    case "fall":vy+=1200*dt;y+=vy*dt;x+=vx*dt;if(y>=floor){y=floor;vy=0;enter("land");}break;
    case "land":if(timer>.28f)enter("idle");break;
    case "walk":x+=vx*dt*(energy<20?.45f:1);if(x<=0||x>=right){x=Math.max(0,Math.min(right,x));enter(energy>20?"climb":"sit");vx=-vx;}else if(timer>(personality==4?1.5f:4))enter("sit");break;
    case "climb":y-=85*dt;if(y<=0){y=0;enter("hang");}break;
    case "hang":if(timer>2.2f){vx=x<right/2?65:-65;vy=0;enter("fall");}break;
    case "sit":if(timer>(personality==4?8:3))enter("idle");break;
    default:if(y<floor-2)enter("fall");else if(timer>2){if(energy<(personality==4?35:10)){sleeping=true;save();}else if(food<20)enter("sit");else{vx=x>right/2?-65:65;enter("walk");}}break;
   }
  }
  x=Math.max(0,Math.min(right,x));y=Math.max(0,Math.min(floor,y));lp.x=Math.round(x);lp.y=Math.round(y);try{wm.updateViewLayout(pet,lp);}catch(IllegalArgumentException e){stopSelf();}pet.invalidate();
 }
 void care(String action){updateNeeds();if(action.equals("feed")){food=clamp(food+25);mood=clamp(mood+5);heart=2;}if(action.equals("pet")){mood=clamp(mood+(personality==1?4:personality==2?20:12));heart=personality==1?.7f:personality==3?4:2.5f;}if(action.equals("sleep")){sleeping=!sleeping;enter(sleeping?"sleep":"fall");vy=0;}save();if(meters!=null)meters.setText(stats());}
 void closePanel(){if(panel!=null){try{wm.removeView(panel);}catch(IllegalArgumentException ignored){}panel=null;meters=null;}}
 void showPanel(){closePanel();panel=new LinearLayout(this);panel.setOrientation(LinearLayout.VERTICAL);int pad=(int)(12*getResources().getDisplayMetrics().density);panel.setPadding(pad,pad,pad,pad);panel.setBackgroundColor(Color.rgb(255,246,226));try(java.io.InputStream in=getAssets().open(new String[]{"theme_cozy.png","theme_pastel.png","theme_fantasy.png"}[theme])){android.graphics.drawable.BitmapDrawable bg=new android.graphics.drawable.BitmapDrawable(getResources(),BitmapFactory.decodeStream(in));bg.setFilterBitmap(false);panel.setBackground(bg);}catch(java.io.IOException ignored){}
  TextView title=new TextView(this);title.setText("🐾 "+petName);title.setTextColor(Color.BLACK);title.setTextSize(18);panel.addView(title);meters=new TextView(this);meters.setTextColor(Color.DKGRAY);meters.setText(stats());panel.addView(meters);
  action("🍗 Alimentar",()->care("feed"));action("♥ Fazer carinho",()->care("pet"));action(sleeping?"☀ Acordar":"☾ Dormir",()->{care("sleep");closePanel();});action("Fechar",()->{closePanel();enter(sleeping?"sleep":"fall");vy=0;});
  int pw=Math.min(width,(int)(250*getResources().getDisplayMetrics().density));WindowManager.LayoutParams p=new WindowManager.LayoutParams(pw,WindowManager.LayoutParams.WRAP_CONTENT,WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE|WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL,PixelFormat.TRANSLUCENT);p.gravity=Gravity.CENTER;
  try{wm.addView(panel,p);}catch(RuntimeException e){panel=null;meters=null;}
 }
 void action(String label,Runnable run){Button b=new Button(this);b.setText(label);panel.addView(b);b.setOnClickListener(v->run.run());}
 public void onDestroy(){handler.removeCallbacksAndMessages(null);updateNeeds();save();closePanel();if(registered)unregisterReceiver(screen);if(pet!=null){try{wm.removeView(pet);}catch(IllegalArgumentException ignored){}pet=null;}super.onDestroy();}
 class PetView extends View {
  Bitmap[] sheets=new Bitmap[catalog.entries.size()];Paint p=new Paint();final Rect src=new Rect();final RectF dst=new RectF();
  PetView(){super(PetService.this);load();}
  void load(){setContentDescription(petName+", toque para cuidar e arraste para brincar");setClickable(true);try{for(int i=0;i<sheets.length;i++){PetCatalog.Entry spec=catalog.get(i);try(java.io.InputStream in=getAssets().open(spec.file)){Bitmap raw=BitmapFactory.decodeStream(in);if(raw==null||raw.getHeight()!=spec.frameHeight||raw.getWidth()%spec.frameWidth!=0)throw new java.io.IOException("Invalid sprite sheet: "+spec.file);sheets[i]=Appearance.recolor(raw,spec.recolor?fur:0,spec.eyes?eyes:0,spec.frameWidth);}}}catch(java.io.IOException e){stopSelf();}}

  protected void onDraw(Canvas c){Bitmap b=sheets[skin];if(b==null)return;PetCatalog.Entry spec=catalog.get(skin);int fw=spec.frameWidth,fh=spec.frameHeight;int frame=(int)(clock*(sleeping?2:spec.fps))%(b.getWidth()/fw);c.save();float bounce=state.equals("walk")?(float)Math.sin(clock*18)*size*.025f:0;float angle=state.equals("climb")?(x<width/2?-18:18):state.equals("drag")?(float)Math.sin(clock*8)*12:0;c.rotate(angle,size/2f,size/2f);if(vx<0)c.scale(-1,1,size/2f,size/2f);float sy=state.equals("land")?.82f:sleeping?.8f:1;c.scale(1,sy,size/2f,size);p.setFilterBitmap(false);float dw=size*Math.min(1,fw/(float)fh),dh=size*Math.min(1,fh/(float)fw);src.set(frame*fw,0,frame*fw+fw,fh);dst.set((size-dw)/2,size-dh+bounce,(size+dw)/2,size+bounce);c.drawBitmap(b,src,dst,p);if(spec.accessories)Appearance.outfit(c,p,outfit,size);c.restore();
   String badge=heart>0?(personality==1?"!":"♥"):sleeping?"Zzz":food<25?"🍗":energy<20?"☾":"";if(!badge.isEmpty()){p.setTextSize(size*.23f);p.setColor(heart>0?Color.rgb(230,70,110):Color.rgb(96,70,130));p.setTypeface(Typeface.DEFAULT_BOLD);p.setShadowLayer(2,0,0,Color.WHITE);c.drawText(badge,size*.52f,size*.24f,p);p.clearShadowLayer();}
  }
  public boolean onTouchEvent(MotionEvent e){switch(e.getActionMasked()){
   case MotionEvent.ACTION_DOWN:closePanel();dragging=true;moved=false;downX=e.getRawX();downY=e.getRawY();startX=x;startY=y;return true;
   case MotionEvent.ACTION_MOVE:float dx=e.getRawX()-downX,dy=e.getRawY()-downY;if(Math.hypot(dx,dy)>10*getResources().getDisplayMetrics().density)moved=true;if(moved){enter("drag");x=startX+dx;y=startY+dy;}return true;
   case MotionEvent.ACTION_UP:case MotionEvent.ACTION_CANCEL:dragging=false;if(!moved&&e.getActionMasked()==MotionEvent.ACTION_UP){performClick();}else{vy=0;vx=x<width/2?65:-65;if(sleeping)enter("sleep");else if(x<12||x>width-size-12)enter("climb");else enter("fall");}return true;
  }return true;}
  public boolean performClick(){super.performClick();care("pet");showPanel();return true;}
 }
}

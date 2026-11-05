package com.catpack.pet;
import android.graphics.*;
final class Appearance {
 static Bitmap recolor(Bitmap original,int fur,int eyes,int frameWidth){Bitmap b=original.copy(Bitmap.Config.ARGB_8888,true);int[] eyeColors={0,0xff229958,0xff367de0,0xffad6b00};int[][] palettes={{},{161,168,184},{215,151,75},{243,243,248},{192,161,223}};
  for(int y=0;y<b.getHeight();y++)for(int x=0;x<b.getWidth();x++){int c=b.getPixel(x,y),r=Color.red(c),g=Color.green(c),bl=Color.blue(c),fx=x%frameWidth;if(Color.alpha(c)==0)continue;
   if(frameWidth==32&&eyes>0&&y>=12&&y<=13&&((fx>=7&&fx<=8)||(fx>=14&&fx<=15))&&r<60&&g<60&&bl<60){b.setPixel(x,y,eyeColors[eyes]);continue;}
   if(fur>0&&r>220&&g>175&&bl>145&&r>=g){int[] p=palettes[fur];float shade=(r+g+bl)/3f/240f;b.setPixel(x,y,Color.rgb(Math.min(255,(int)(p[0]*shade)),Math.min(255,(int)(p[1]*shade)),Math.min(255,(int)(p[2]*shade))));}
  }return b;
 }
 static void outfit(Canvas c,Paint p,int outfit,float size){if(outfit==0)return;c.save();c.scale(size/32,size/32);p.setStyle(Paint.Style.FILL);p.setColor(0xff28212d);
  if(outfit==1){c.drawRect(5,18,17,20,p);p.setColor(0xffd54e58);c.drawRect(6,18,16,19,p);p.setColor(0xffffcd60);c.drawRect(10,19,12,21,p);}
  if(outfit==2){p.setColor(0xffe46a9a);Path b=new Path();b.moveTo(14,5);b.lineTo(19,7);b.lineTo(23,4);b.lineTo(23,10);b.lineTo(19,8);b.lineTo(14,10);b.close();c.drawPath(b,p);p.setColor(0xff9c3668);c.drawRect(18,6,20,9,p);}
  if(outfit==3){p.setColor(0xff7359a7);Path hat=new Path();hat.moveTo(4,7);hat.lineTo(12,0);hat.lineTo(18,7);hat.close();c.drawPath(hat,p);p.setColor(0xff4f397e);c.drawRect(3,6,20,8,p);p.setColor(0xffffd979);c.drawRect(11,3,13,5,p);}
  if(outfit==4){p.setColor(0xff477ab7);c.drawRect(6,20,17,26,p);c.drawRect(4,21,7,24,p);c.drawRect(17,21,19,24,p);p.setColor(0xffffdb8d);c.drawRect(10,22,13,24,p);}
  c.restore();
 }
}

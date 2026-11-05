package com.catpack.pet;
import android.content.Context;
import org.json.*;
import java.util.*;
import java.io.*;

/** Horizontal sprite strips, described by assets/pets.json. No fixed character count. */
final class PetCatalog {
 static final class Entry {
  final String id,name,file; final int frameWidth,frameHeight; final float fps;
  final boolean recolor,eyes,accessories;
  Entry(JSONObject o) throws JSONException {
   id=o.getString("id");name=o.getString("name");file=o.getString("file");
   frameWidth=o.getInt("frameWidth");frameHeight=o.getInt("frameHeight");fps=(float)o.optDouble("fps",8);
   recolor=o.optBoolean("recolor",false);eyes=o.optBoolean("eyes",false);accessories=o.optBoolean("accessories",false);
   if(frameWidth<1||frameHeight<1||fps<=0||file.contains("..")||file.startsWith("/"))throw new JSONException("Invalid character: "+id);
  }
 }
 final ArrayList<Entry> entries=new ArrayList<>();
 PetCatalog(Context context){try(InputStream in=context.getAssets().open("pets.json")){
  ByteArrayOutputStream data=new ByteArrayOutputStream();byte[] buffer=new byte[4096];int n;while((n=in.read(buffer))!=-1)data.write(buffer,0,n);
  JSONArray array=new JSONArray(data.toString("UTF-8"));for(int i=0;i<array.length();i++)entries.add(new Entry(array.getJSONObject(i)));
  if(entries.isEmpty())throw new JSONException("Empty character catalog");
 }catch(IOException|JSONException e){throw new IllegalStateException("Invalid assets/pets.json",e);}}
 String[] names(){String[] result=new String[entries.size()];for(int i=0;i<result.length;i++)result[i]=entries.get(i).name;return result;}
 int safeIndex(int index){return Math.max(0,Math.min(entries.size()-1,index));}
 Entry get(int index){return entries.get(safeIndex(index));}
}

package com.catpack.pet;
import android.content.*;import org.json.*;import java.io.*;
/** Seed a new personalized app exactly once; never overwrite an existing pet. */
final class ProfileDefaults {
 static void ensure(Context context){SharedPreferences prefs=context.getSharedPreferences("config",0);if(prefs.getBoolean("seeded",false))return;
  try(InputStream in=context.getAssets().open("defaults.json")){ByteArrayOutputStream data=new ByteArrayOutputStream();byte[] buf=new byte[2048];int n;while((n=in.read(buf))!=-1)data.write(buf,0,n);JSONObject o=new JSONObject(data.toString("UTF-8"));SharedPreferences.Editor edit=prefs.edit();if(!prefs.contains("name"))edit.putString("name",o.optString("name","Mingau"));for(String key:new String[]{"sex","personality","skin","fur","eyes","outfit","theme","size"})if(!prefs.contains(key)&&o.has(key))edit.putInt(key,o.getInt(key));edit.putBoolean("seeded",true).apply();
  }catch(IOException|JSONException e){prefs.edit().putBoolean("seeded",true).apply();}
 }
}

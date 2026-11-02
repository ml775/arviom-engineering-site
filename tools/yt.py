import json,uuid,urllib.request,urllib.parse,sys
from lib import api
CRED={"youTubeOAuth2Api":{"id":"M1mSo2Os1membl4N","name":"YouTube account"}}
def wf():
  p='yt-'+uuid.uuid4().hex[:12]
  w={"name":"Webhook","type":"n8n-nodes-base.webhook","typeVersion":2,"position":[0,0],"id":str(uuid.uuid4()),"webhookId":str(uuid.uuid4()),"parameters":{"path":p,"httpMethod":"GET","responseMode":"lastNode","options":{}}}
  h={"name":"YT","type":"n8n-nodes-base.httpRequest","typeVersion":4.2,"position":[250,0],"id":str(uuid.uuid4()),"credentials":CRED,
     "parameters":{"url":"={{ 'https://www.googleapis.com/youtube/v3/' + $json.query.u }}","authentication":"predefinedCredentialType","nodeCredentialType":"youTubeOAuth2Api","options":{"response":{"response":{"neverError":True}}}}}
  c=api('POST','/workflows',{"name":"TMP yt read","nodes":[w,h],"settings":{"executionOrder":"v1"},"connections":{"Webhook":{"main":[[{"node":"YT","type":"main","index":0}]]}}})
  api('POST','/workflows/%s/activate'%c['id']);return c['id'],p
def run():
  wid,p=wf()
  g=lambda u: json.loads(urllib.request.urlopen('https://n8n.arviom.com.ua/webhook/'+p+'?'+urllib.parse.urlencode({'u':u}),timeout=60).read())
  try:
    c=g('channels?part=snippet,statistics,contentDetails&mine=true'); c=c[0] if isinstance(c,list) else c
    if not c.get('items'): print('NO CHANNEL', json.dumps(c)[:600]); return
    for it in c['items']: print('CHANNEL',it['id'],it['snippet']['title'],it['statistics'])
    up=c['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    v=g('playlistItems?part=snippet&maxResults=50&playlistId='+up); v=v[0] if isinstance(v,list) else v
    for it in v.get('items',[]): print(it['snippet']['publishedAt'][:10],it['snippet']['resourceId']['videoId'],it['snippet']['title'])
    pl=g('playlists?part=snippet,contentDetails&mine=true&maxResults=50'); pl=pl[0] if isinstance(pl,list) else pl
    for it in pl.get('items',[]): print('PLAYLIST',it['id'],it['snippet']['title'],it['contentDetails']['itemCount'])
  finally: api('DELETE','/workflows/'+wid)
if __name__=='__main__': run()

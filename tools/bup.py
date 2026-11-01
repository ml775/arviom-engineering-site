import sys,json,uuid,urllib.request,os,mimetypes
from lib import api
B='https://n8n.arviom.com.ua/webhook/'
CR={"googleDriveOAuth2Api":{"id":"bgRHLARdjTNkctc2","name":"Google Drive account"}}
def wh(path): return {"name":"Webhook","type":"n8n-nodes-base.webhook","typeVersion":2,"position":[0,0],"id":str(uuid.uuid4()),"webhookId":str(uuid.uuid4()),"parameters":{"path":path,"httpMethod":"POST","responseMode":"lastNode","options":{}}}
def make():
  p1='bf-'+uuid.uuid4().hex[:12]; p2='bu-'+uuid.uuid4().hex[:12]
  fold={"name":"Drive","type":"n8n-nodes-base.httpRequest","typeVersion":4.2,"position":[250,0],"id":str(uuid.uuid4()),"credentials":CR,
   "parameters":{"method":"POST","url":"https://www.googleapis.com/drive/v3/files?fields=id,webViewLink","authentication":"predefinedCredentialType","nodeCredentialType":"googleDriveOAuth2Api","sendBody":True,"specifyBody":"json","jsonBody":"={{ JSON.stringify($json.body) }}","options":{}}}
  up={"name":"Drive","type":"n8n-nodes-base.googleDrive","typeVersion":3,"position":[250,0],"id":str(uuid.uuid4()),"credentials":CR,
   "parameters":{"operation":"upload","name":"={{ $json.query.name }}","driveId":{"__rl":True,"mode":"list","value":"My Drive"},"folderId":{"__rl":True,"mode":"id","value":"={{ $json.query.parent }}"},"inputDataFieldName":"file","options":{}}}
  ids=[]
  for p,n in ((p1,fold),(p2,up)):
    wf={"name":"TMP brand upload","nodes":[wh(p),n],"settings":{"executionOrder":"v1"},"connections":{"Webhook":{"main":[[{"node":"Drive","type":"main","index":0}]]}}}
    c=api('POST','/workflows',wf); api('POST','/workflows/%s/activate'%c['id']); ids.append(c['id'])
  json.dump({"ids":ids,"fold":p1,"up":p2},open('bup.state','w')); print(ids)
def post(url,data,ct):
  r=urllib.request.Request(url,data=data,method='POST',headers={'Content-Type':ct}); return json.loads(urllib.request.urlopen(r,timeout=120).read() or b'{}')
def folder(name,parent=None):
  st=json.load(open('bup.state')); b={"name":name,"mimeType":"application/vnd.google-apps.folder"}
  if parent: b["parents"]=[parent]
  print(json.dumps(post(B+st['fold'],json.dumps(b).encode(),'application/json')))
def upload(path,parent,name=None):
  st=json.load(open('bup.state')); name=name or os.path.basename(path)
  bd='----b'+uuid.uuid4().hex; mt=mimetypes.guess_type(path)[0] or 'application/octet-stream'
  data=('--%s\r\nContent-Disposition: form-data; name="file"; filename="%s"\r\nContent-Type: %s\r\n\r\n'%(bd,os.path.basename(path),mt)).encode()+open(path,'rb').read()+('\r\n--%s--\r\n'%bd).encode()
  import urllib.parse; q=urllib.parse.urlencode({'name':name,'parent':parent})
  r=post(B+st['up']+'?'+q,data,'multipart/form-data; boundary='+bd); r=r[0] if isinstance(r,list) else r
  print(name, r.get('id'), r.get('error') or '')
def clean():
  for i in json.load(open('bup.state'))['ids']: api('DELETE','/workflows/'+i)
  print('deleted')
if __name__=='__main__':
  a=sys.argv; {'make':lambda:make(),'folder':lambda:folder(a[2],a[3] if len(a)>3 else None),'upload':lambda:upload(a[2],a[3],a[4] if len(a)>4 else None),'clean':lambda:clean()}[a[1]]()

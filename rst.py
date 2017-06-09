# -*- coding: cp1252 -*-
import android, pprint, time, os
droid = android.Android()

email=''
phone=''
reset=''
apaga=''
localiza=''

def main():
  global email, phone, reset, apaga, localiza
  try:
    arqpath = '/storage/config.txt'
    if os.path.isfile(arqpath):
      arq=open(arqpath, 'r').readlines()
      
      if 'config=1\n' in arq:
        cfg = open(arqpath, 'r').readlines()
        email = cfg[1].rstrip().split('=')[1]
        phone = cfg[2].rstrip().split('=')[1]
        reset = cfg[3].rstrip().split('=')[1]
        apaga = cfg[4].rstrip().split('=')[1]
        localiza = cfg[5].split('=')[1]
        loop()
        
      elif 'config=0\n' or '' in arq:
        cfg = open(arqpath, 'w')
        config='config=1'
        email='email='+droid.dialogGetInput('Digite o email:', 'Onde serao enviado os dados').result
        phone='phone='+droid.dialogGetInput('Digite o Telefone', 'Ex:45999530893 para receber os dados').result
        reset='reset='+droid.dialogGetInput('Msg Reset', 'Digite a Msg de Reset de Configuracao').result
        delete='apaga='+droid.dialogGetInput('Apagar Msg', 'Digite a msg que apaga os rastros').result
        local='localiza='+droid.dialogGetInput('Localizar', 'Msg para localizar o aparelho').result
        cfg.write(config+'\n')
        cfg.write(email+'\n')
        cfg.write(phone+'\n')
        cfg.write(reset+'\n')
        cfg.write(delete+'\n')
        cfg.write(local)
        cfg.close()
        main()
        
    else:
      arq = open(arqpath, 'a')
      arq.close()
      main()
      
  except:
    print("Erro no sistema1, Re instale o APK")
    

def loop():
  global localiza, apaga, reset
  try:
    path = '/storage/smsid.txt'
    if not os.path.isfile(path):
      arq = open(path, 'a')
      main()
        
    arq = open(path, 'r').read().split('\n')
    while True:
      msg = droid.smsGetMessageIds(False, 'inbox').result
      if msg != []:
        for smsid in msg:
          sm = droid.smsGetMessageById(smsid).result
          if sm['address'][-9::] == phone[-9::]:
              
            if sm['body'].lower() == localiza.lower():
              if not sm['date'] in arq:
                arq = open(path, 'a')
                arq.write(sm['date']+'\n')
                arq.close()
                return gps(smsid)
                
            elif sm['body'].lower() == apaga.lower():
              if not sm['date'] in arq:
                arq = open(path, 'a')
                arq.write(sm['date']+'\n')
                arq.close()
                return delete(smsid)

            elif sm['body'].lower() == reset.lower():
              if not sm['date'] in arq:
                arq = open(path, 'a')
                arq.write(sm['date']+'\n')
                arq.close()
                return resetar()
              
  except:
    print("Erro no sistema2, Re instale o APK")
          
  main()

def resetar():
  arqpath = '/storage/config.txt'
  if os.path.isfile(arqpath):
    os.remove(arqpath)
    main()
  main()

def delete(smsid):
  sms = droid.smsGetMessageIds(True, 'sent').result
  if sms != []:
    for msg in sms:
      ss = droid.smsGetMessageById(msg).result
      if ss['address'][-9::] == phone[-9::]:
        if droid.smsDeleteMessage(msg).result:
          delete()
  main()
  
def gps(smid):
  while True:
    droid.toggleWifiState(True)
    local = droid.startLocating()
    time.sleep(10)
    event=droid.readLocation().result
    if event != {}:    
      latitude=event['gps']['latitude']
      longitude=event['gps']['longitude']
      return send(smid, latitude, longitude)
    
    elif event != {}:
      latitude=event['network']['latitude']
      longitude=event['network']['longitude']
      return send(smid, latitude, longitude)
      
def send(ss, lat, lon):
  global email
  try:
    msg='Aparelho Localizado:Latitude: %s Longitude: %s'%(str(lat), str(lon))
    tel = '9090'+phone[-9::]
    droid.smsSend(phone[-9::], msg)
    droid.smsSend(tel, msg)
    droid.smsDeleteMessage(ss)
    droid.sendEmail(email, 'Rastreador', msg)
    main()
  except:
    print("Erro no sistema3, Re instale o APK")
    main()
    
main()

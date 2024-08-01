from __future__ import print_function
from gnr.web.batch.btcaction import BaseResourceAction
from decimal import Decimal
from time import sleep
import os 
from gnr.core.gnrnumber import floatToDecimal,decimalRound

caption = 'Saldo multiplo' #nome nel menu dei batch
tags = 'admin,user'  #autorizzazione al batch
description =  'Saldo di più fatture' #nome piu completo

class Main(BaseResourceAction):
    batch_prefix = 'agg' #identificatore di batch (univoco)
    batch_title = 'Saldo fatture' #titolo all'interno del visore del batch
    batch_delay = 0.5  #periodo campionamento termometro
    batch_steps='main'
    batch_cancellable = True
    virtual_columns = '$saldo'
    #batch_selection_savedQuery = 'testbatch'

    def step_main(self):
        print('page_id',self.db.currentPage.page_id)
        selection = self.get_selection()#(columns='$id,$doc_n,$importo,$saldo')
        
        if not selection:
            self.batch_debug_write('Nessun record trovato')
            return
        data_saldo = self.batch_parameters.get('data_saldo')
        imp_pag = self.batch_parameters.get('imp_pag')
        note = self.batch_parameters.get('note')
        
        records = self.get_records(for_update=True) #dalla selezione corrente ottiene un iteratore in formato record
        
        maximum = len(self.get_selection())
        iteratore_fatemesse = self.btc.thermo_wrapper(records,message=self.messaggio_termometro, maximum=maximum) 
        
        #il metodo thermo_wrapper ottiene un iteratore che scorrendo ogni elemento aggiorna il termometro 
        #con il ciclo for successivo aggiorniamo il pagamento delle fatture selezionate
        nuovo_pagcliente=None
        saldo_fat=0
        rim_pag=imp_pag
        my_records=[]
        for record in iteratore_fatemesse:
            my_records.append(dict(doc_n=record['doc_n'], data=record['data'], importo=record['importo'],saldo=record['saldo'],cliente_id=record['cliente_id'],id=record['id']))
        my_rec=sorted(my_records, key=lambda x:(x['doc_n'],x['data']))
        
        #for c,record in enumerate(my_rec):
        for record in my_rec:
            saldo_fat -= record['saldo']
            cliente_id = record['cliente_id']
            saldo = record['saldo']
            #print(record['doc_n'])
            if saldo > 0:
                if saldo >= imp_pag:
                    rim_pag = imp_pag - imp_pag
                    
                    fatemesse_id = record['id']
                    nuovo_pagcliente = self.db.table('acc_mp.pag_fat_emesse').newrecord(fatt_emesse_id=fatemesse_id, data=data_saldo, importo=imp_pag, note=note)
                    self.db.table('acc_mp.pag_fat_emesse').insert(nuovo_pagcliente)
                    #if nuovo_pagcliente:
                    #    self.db.commit()
                    if rim_pag == 0:
                        break
                else:

                    if rim_pag >= saldo:
                        imp_saldo = saldo  
                        imp_pag = rim_pag - saldo
                        
                    else:
                        imp_saldo = rim_pag
                        imp_pag = imp_pag - rim_pag    
                    
                    rim_pag = rim_pag - imp_saldo
                    
                    fat_id = record['id']
                    nuovo_pagcliente = self.db.table('acc_mp.pag_fat_emesse').newrecord(fatt_emesse_id=fat_id, data=data_saldo, importo=imp_saldo, note=note)
                    #print(c)
                    self.db.table('acc_mp.pag_fat_emesse').insert(nuovo_pagcliente)
        #se abbiamo un pagamento maggiore delle fatture selezionate sull'ultima fattura sarà inserito il maggior pagamento
        if rim_pag > 0:
            nuovo_pagcliente = self.db.table('acc_mp.pag_fat_emesse').newrecord(fatt_emesse_id=fat_id, data=data_saldo, importo=rim_pag, note=note)
            #print(c)
            self.db.table('acc_mp.pag_fat_emesse').insert(nuovo_pagcliente)    
                    #if nuovo_pagcliente:
                    #    self.db.commit()
          # print('rim_pag='+str(rim_pag))
          # print('imp_pag'+str(imp_pag))
          # print('imp_saldo'+str(imp_saldo))

        #verifichiamo il totale delle fatture cliente poi preleviamo tutti gli id delle fatture cliente che con un ciclo for nella tbl 
        # pagamenti cliente andremo a calcolare il totale pagato per poi calcolare il saldo
        totale_fatture = self.db.table('acc_mp.fat_emesse').readColumns(columns="""SUM($importo) AS totale_fatture""",
                                                                     where='$cliente_id=:c_id',c_id=cliente_id)
        fatture_cliente_id = self.db.table('acc_mp.fat_emesse').query(columns='$id',where='$cliente_id=:c_id', c_id=cliente_id).fetchAsDict('id')
        totale_pagato = 0
        #for a in fatture_cliente_id:
        #    pagamenti = self.db.table('acc_mp.pag_fat_emesse').query(columns='$importo',
        #                                                        where='$fatt_emesse_id=:fe_id', fe_id=a).fetch()
        #    #for r in range(len(pagamenti)-1):
        #    #    totale_pagato += pagamenti[0][r]
        #    for r in pagamenti:
        #        totale_pagato += pagamenti[0][0]

        tbl_pagamenti = self.db.table('acc_mp.pag_fat_emesse')
        totale_pagato = tbl_pagamenti.readColumns(columns="""SUM($importo)""", where='@fatt_emesse_id.cliente_id=:id_cl', id_cl=cliente_id)

        #prendiamo il record della tabella cliente e con for_update=True successivamente faremo l'aggiornamento con il nuovo saldo 
        tbl_cliente = self.db.table('acc_mp.cliente')
        record_cliente = tbl_cliente.record(where='$id=:id_cliente', 
                                  id_cliente=cliente_id,
                                  for_update=True).output('dict')
        old_record = dict(record_cliente)
        tbl_imb = self.db.table('acc_mp.imbarcazione')
        imb_id = selection.data[0][6]
        nome_imb = tbl_imb.readColumns(columns="$nome", where='$id=:id_imb', id_imb=imb_id)
        if totale_fatture is not None:
            #if rim_pag > 0:
            #    note=old_record['note']
            #    if note is None:
            #        note=''
            #    nuovo_record = dict(id=cliente_id,note=str(note) + ' ' + str(nome_imb) +' - maggior pagamento di € '+str(rim_pag),balance=floatToDecimal(totale_fatture - totale_pagato or 0))
            #else:
            nuovo_record = dict(id=cliente_id,balance=floatToDecimal(totale_fatture - totale_pagato or 0))
            tbl_cliente.update(nuovo_record,old_record)
        #print(X)
        if nuovo_pagcliente:
            self.db.commit()       

    def messaggio_termometro(self,record, curr, tot, **kwargs):
        return "Invoice %s %i/%i" %(record['doc_n'],curr,tot)

    def table_script_parameters_pane(self,pane,extra_parameters=None,record_count=None,**kwargs):
        fb = pane.formbuilder(cols=1,border_spacing='3px')
        fb.dateTextBox(value='^.data_saldo',lbl='!![it]Data pagamento')
        fb.currencyTextBox(value='^.imp_pag', lbl='!![it]Importo versato', format='#,###.00')
        fb.simpleTextArea(value='^.note',lbl='!![en]Note')
        fb.div(f'Applica il saldo a {record_count} fatture')

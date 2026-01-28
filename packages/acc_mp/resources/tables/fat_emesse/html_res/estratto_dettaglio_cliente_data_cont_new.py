from gnr.web.gnrbaseclasses import TableScriptToHtml
from datetime import datetime
import pandas as pd
from collections import defaultdict

class Main(TableScriptToHtml):
    maintable = 'acc_mp.fat_emesse'
    row_table = 'acc_mp.fat_emesse'
    css_requires='grid'
    page_width = 297
    page_height = 210
    page_margin_left = 5
    page_margin_right = 5
    
    doc_footer_height = 15
    doc_header_height = 16
    grid_row_height = 5
    grid_header_height = 5
    totalize_footer='Totale'
    cliente_height = 10
    #Fornendo a totalize_footer una stringa testuale, questa verrà usata come etichetta della riga di totalizzazione
    empty_row=dict()
    #Grazie a questo parametro in caso di mancanza di dati verrà stampata una griglia vuota invece di una pagina bianca
    virtual_columns = '@fatt_emesse_id.tot_pag,@fatt_emesse_id.saldo' #aggiungiamo le colonne calcolate

    def docHeader(self, header):
        #Questo metodo definisce il layout e il contenuto dell'header della stampa
        
        #if len(self.cliente_id) > 1:
        #    cliente=''
        #else:
        #    cliente= self.rowField('cliente')   
        if self.parameter('cliente_id'):
            cliente=self.rowField('cliente')
        else:
            cliente= ''
        head = header.layout(name='doc_header', margin='5mm', border_width=0)
        row = head.row()
        if self.parameter('anno'):
            row.cell("""<center><div style='font-size:14pt;'><strong>Estratto/Statement {anno}<br>{cliente}</strong></div></center>::HTML""".format(cliente=cliente,anno=self.parameter('anno')))
        elif self.parameter('dal'):
            row.cell("""<center><div style='font-size:12pt;'><strong>Estratto/Statement from {dal} to {al}<br>{cliente}</strong></div>
                    </center>::HTML""".format(cliente=cliente,dal=self.parameter('dal').strftime("%d/%m/%Y"),al=self.parameter('al').strftime("%d/%m/%Y")))            
        else:
            #row = head.row()
            row.cell("""<center><div style='font-size:14pt;'><strong>Estratto/Statement</strong></div>
                    <div style='font-size:12pt;'><strong>{cliente}</strong></div></center>::HTML""".format(
                                cliente=cliente))

    def defineCustomStyles(self):
        #Questo metodo definisce gli stili del body dell'html
        self.body.style(""".cell_label{
                            font-size:8pt;
                            text-align:left;
                            color:grey;
                            text-indent:1mm;}

                            .footer_content{
                            text-align:right;
                            margin:2mm;
                            font-size:8pt;
                            }
                            """)

    def gridStruct(self,struct):
        #Questo metodo definisce la struttura della griglia di stampa definendone colonne e layout
        r = struct.view().rows()
        #if len(self.cliente_id) > 1:
        #    r.cell('cliente',mm_width=30)
        if not self.parameter('cliente_id'):
            r.cell('cliente',mm_width=100, content_class="breakword", name='Cliente')
            r.cell('cliente', hidden=True, subtotal='Totali {breaker_value}',subtotal_order_by='$cliente',subtotal_content_class='color_cell')    
        r.cell('data', mm_width=15, name='Data fat.')
         #r.fieldcell('mese_fattura', hidden=True, subtotal='Totale {breaker_value}', subtotal_order_by="$data")
         #Questa formulaColumn verrà utilizzata per creare i subtotali per mese
        r.cell('doc_n', mm_width=15, name='Fattura n.')
        #r.cell('doc_n', hidden=True, subtotal='Totale documento {breaker_value}',subtotal_order_by='$cliente')
        #r.fieldcell('cliente_id', mm_width=0)
        
        r.cell('imbarcazione',mm_width=0,name='Nome imbarcazione', content_class="breakword")
        r.cell('importo', mm_width=20, name='Importo fat.', totalize=True,format='#,###.00')
        r.cell('pagamento_data', mm_width=15, name='Data pag.')
        r.cell('pagamento_importo', mm_width=20, name='Importo pag.', totalize=True,format='#,###.00')
        r.cell('note',mm_width=0,name='Note')
        r.cell('balance', mm_width=20, name='Rimanenza fat.', format='#,###.00')
        r.cell('saldo_finale', mm_width=20, name='Rimanenza', totalize=True,format='#,###.00')
        
        #r.cell('saldo',name='Saldo avere', mm_width=20, totalize=True,format='#,###.00')
        #r.cell('balance_cliente',name='Balance totale',mm_width=20,format='#,###.00', totalize=True)
        
    def calcRowHeight(self):
        #Determina l'altezza di ogni singola riga con approssimazione partendo dal valore di riferimento grid_row_height
        cliente_offset = 30
        imbarcazione_offset = 15
        #Stabilisco un offset in termini di numero di caratteri oltre il quale stabilirò di andare a capo.
        #Attenzione che in questo caso ho una dimensione in num. di caratteri, mentre la larghezza della colonna è definita
        #in mm, e non avendo utti i caratteri la stessa dimensione si tratterà quindi di individuare la migliore approssimazione
        if not self.parameter('cliente_id'):
            n_rows_cliente = len(self.rowField('cliente'))//cliente_offset
        else:
            n_rows_cliente = len(self.rowField('cliente'))//cliente_offset     
        n_rows_imb = len(self.rowField('imbarcazione'))//imbarcazione_offset + 1.2

      
  #      n_rows_nome_provincia = len(self.rowField('_sigla_provincia_nome'))//nome_offset + 1
        #In caso di valori in relazione, è necessario utilizzare "_" nel metodo rowField per recuperare correttamente i valori
        #A tal proposito si consiglia comunque sempre di utilizzare le aliasColumns
        n_rows = max(n_rows_cliente,n_rows_imb)#, n_rows_nome_provincia)
        height = (self.grid_row_height * n_rows)
        return height
    
    def gridData(self): 
        
        #if self.parameter('anno'):
        #    year_v= self.parameter('anno')
        #    datasaldo=datetime.strptime(year_v+'-12-31', '%Y-%m-%d').date()
        #    self.page.pageStore().setItem('data_saldo',datasaldo)
        #else:
        #    self.page.pageStore().setItem('data_saldo',self.parameter('al'))
        condition=[]
        if self.parameter('cliente_id'):
                condition = ['$cliente_id=:cliente_id']       
        #condition_pag = ['fatt_emesse_id=:fatemesse_id']
        condition_pag = []
        balance=0
        if self.parameter('balance') == True:

           condition.append('$saldo>:balance')
        #else:
        #    condition.append('$saldo>=:balance')    
        if self.parameter('anno'):
            condition.append('$anno_doc=:anno')
            condition_pag.append('$anno_doc=:anno')
        if self.parameter('dal') and self.parameter('al'):
            condition.append('$data BETWEEN :dal AND :al')
            condition_pag.append('$data BETWEEN :dal AND :al')
         
        where = ' AND '.join(condition)
        where_pag = ' AND '.join(condition_pag)
        
        fat_emesse = self.db.table('acc_mp.fat_emesse').query(columns="""@cliente_id.rag_sociale,
                                            $data,$doc_n,@imbarcazione_id.nome,$importo,$tot_pag,$saldo""",
                                            where=where,
                                            balance=balance,
                                            anno=self.parameter('anno'),
                                            dal=self.parameter('dal'),
                                            al=self.parameter('al'),
                                            cliente_id=self.parameter('cliente_id'), 
                                            order_by='@cliente_id.rag_sociale,$data'
                                            ).fetch()   
        pagfatEmesse = self.db.table('acc_mp.pag_fat_emesse').query(columns="""$fatt_emesse_id,@fatt_emesse_id.@cliente_id.rag_sociale,
                                            $data,$importo,$note""",
                                            where=where_pag,
                                            anno=self.parameter('anno'),
                                            dal=self.parameter('dal'),
                                            al=self.parameter('al')).fetch() 
        
        clienti = defaultdict(lambda: {"fatture": {}})
        #print(c)

        # Inserisco le fatture
        for f in fat_emesse:
            clienti[f["_cliente_id_rag_sociale"]]["fatture"][f["pkey"]] = {
                "data": f["data"],
                "doc_n": f["doc_n"],
                "importo": f["importo"],
                "imbarcazione":f["_imbarcazione_id_nome"],
                "pagamenti": []
            }
        # pagamenti è UNA LISTA di dict
        pagamenti_per_fattura = defaultdict(list)

        for p in pagfatEmesse:
            pagamenti_per_fattura[p["fatt_emesse_id"]].append(p)

        # saldo progressivo
        for cliente_data in clienti.values():
            for fattura_id, fattura in cliente_data["fatture"].items():

                saldo = fattura["importo"]  
                pagamenti_ordinati = sorted(
                    pagamenti_per_fattura.get(fattura_id, []),
                    key=lambda x: x["data"]
                )

                for p in pagamenti_ordinati:
                    saldo -= p["importo"]
                    fattura["pagamenti"].append({
                        "data": p["data"],
                        "importo": p["importo"],
                        "note": p.get("note"),
                        "balance": saldo
                    })

                fattura["saldo_finale"] = saldo
        clienti = dict(clienti)
        righe = self.flatten_clienti(clienti)
        self.page.pageStore().setItem('data_saldo',None) #riportiamo il valore a None della data_saldo nella dbEnv
        return righe

    def flatten_clienti(self,clienti):
        righe = []

        for cliente, cdata in clienti.items():
            for fattura_id, f in cdata.get("fatture", {}).items():

                # prima riga: la fattura
                righe.append({
                    "tipo": "fattura",
                    "cliente": cliente,
                    "fattura_id": fattura_id,
                    "data": f.get("data"),
                    "doc_n": f.get("doc_n"),
                    "importo": f.get("importo"),
                    "imbarcazione": f.get("imbarcazione"),
                    "pagamento_data": None,
                    "pagamento_importo": None,
                    "note": None,
                    "balance": None,
                    "saldo_finale": f.get("saldo_finale")
                })

                # righe successive: i pagamenti
                for p in f.get("pagamenti", []):
                    righe.append({
                        "tipo": "pagamento",
                        "cliente": cliente,
                        "fattura_id": fattura_id,
                        "data": None,
                        "doc_n": f.get("doc_n"),
                        "importo": None,
                        "imbarcazione": "pagamento",
                        "pagamento_data": p.get("data"),
                        "pagamento_importo": p.get("importo"),
                        "note": p.get("note"),
                        "balance": p.get("balance"),
                        "saldo_finale": None#f.get("saldo_finale")
                    })

        return righe

    def docFooter(self, footer, lastPage=None):
        #Questo metodo definisce il layout e il contenuto dell'header della stampa
        foo = footer.layout('totali_fattura',top=1,
                           lbl_class='cell_label', 
                           content_class = 'footer_content',border_color='white')
        r = foo.row()
        today = self.db.workdate.strftime("%d/%m/%Y")
        r.cell('Documento stampato il {oggi}'.format(oggi=today))
        
    def outputDocName(self, ext=''):
        #Questo metodo definisce il nome del file di output
        if len(self.gridData())>0:
            cliente=self.gridData()[0]['cliente'].replace('.','').replace(' ','_')
        else:
            cliente=''    
        if ext and not ext[0] == '.':
            ext = '.%s' % ext
        if self.parameter('anno') and self.parameter('cliente_id'):
            doc_name = 'Estratto_{anno}_{cliente}{ext}'.format(anno=self.parameter('anno'), 
                        cliente=cliente, ext=ext)
        elif self.parameter('anno'):
            doc_name = 'Estratto_{anno}{ext}'.format(anno=self.parameter('anno'),ext=ext)    
        elif self.parameter('dal') and self.parameter('al') and self.parameter('cliente_id'):
            doc_name = 'Estratto_dal_{dal}_al_{al}_{cliente}{ext}'.format(dal=self.parameter('dal').strftime("%d-%m-%Y"),
                        al=self.parameter('al').strftime("%d-%m-%Y"),
                        cliente=cliente, ext=ext)   
        elif self.parameter('dal') and self.parameter('al').strftime("%d-%m-%Y"):
            doc_name = 'Estratto_dal_{dal}_al_{al}'.format(dal=self.parameter('dal').strftime("%d-%m-%Y"),
                        al=self.parameter('al').strftime("%d-%m-%Y"), ext=ext)
        elif self.parameter('cliente_id'):
            doc_name = 'Estratto_{cliente}{ext}'.format(cliente=cliente, ext=ext)         
        else: 
            doc_name = 'Estratto'.format(ext=ext)
        return doc_name

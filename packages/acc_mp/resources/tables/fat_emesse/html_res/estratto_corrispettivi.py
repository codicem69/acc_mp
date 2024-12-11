from gnr.web.gnrbaseclasses import TableScriptToHtml
from datetime import datetime

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
    grid_header_height = 10
    grid_style_cell='font-size: 12pt'
    
    totalize_footer='Totale'
    cliente_height = 10
    #Fornendo a totalize_footer una stringa testuale, questa verrà usata come etichetta della riga di totalizzazione
    empty_row=dict()
    #Grazie a questo parametro in caso di mancanza di dati verrà stampata una griglia vuota invece di una pagina bianca
    virtual_columns = '@fatt_emesse_id.tot_pag,@fatt_emmese_id.saldo' #aggiungiamo le colonne calcolate

    def docHeader(self, header):
        #Questo metodo definisce il layout e il contenuto dell'header della stampa
        
        
        head = header.layout(name='doc_header', margin='5mm', border_width=0)
        row = head.row()
        
        row.cell("""<center><div style='font-size:14pt;'><strong>Estratto corrispettivi {data}</strong></div>
                     ::HTML""".format(data=self.parameter('date').strftime("%d-%m-%Y")))

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
    def gridLayout(self,body):
        return body.layout(name='rowsL',um='mm',
                            top=1,bottom=1,left=1,right=1,
                            border_width=.3,
                            style='line-height:5mm;text-align:center;font-size:12pt;')
    
    def gridStruct(self,struct):
        #Questo metodo definisce la struttura della griglia di stampa definendone colonne e layout
        r = struct.view().rows()
        
        r.cell('data', mm_width=15, name='Data')
         #r.fieldcell('mese_fattura', hidden=True, subtotal='Totale {breaker_value}', subtotal_order_by="$data")
         #Questa formulaColumn verrà utilizzata per creare i subtotali per mese
        r.cell('doc_n', mm_width=0, name='Fattura n.', content_class="breakword")
        #r.cell('doc_n', hidden=True, subtotal='Totale documento {breaker_value}',subtotal_order_by='$cliente')
        r.cell('sifiva', mm_width=30, name='Olio Naz./Sif+Iva/Bunker', totalize=True,format='#,###.00')
        r.cell('gasnaz', mm_width=20, name='Gasolio Naz.', totalize=True,format='#,###.00')
        r.cell('benznaz', mm_width=20, name='Benzina Naz.', totalize=True,format='#,###.00')
        r.cell('sif', mm_width=20, name='Prodotto SIF', totalize=True,format='#,###.00')
        r.cell('benz8', mm_width=20, name='Benzina senza IVA', totalize=True,format='#,###.00')
        r.cell('a22', mm_width=20, name='IVA 22%', totalize=True,format='#,###.00')
        r.cell('tot_estratto', mm_width=20, name='Totale giornaliero', totalize=True,format='#,###.00')
          
    
    def gridData(self): 
        condition = []
        
        condition.append('$data=:data')
        where = ' AND '.join(condition)
        
        righe_fat=[]
        righe=[]
        data_report = self.parameter('date')
        fat_emesse = self.db.table('acc_mp.fat_emesse').query(columns="""$data,$doc_n,$importo,$tip_vend""",
                                            where=where,
                                            data=data_report,
                                            order_by='$doc_n').fetch()       
        f_sifiva=0
        f_gasnaz=0
        f_benznaz=0
        f_sif=0
        f_benz8=0
        f_22=0
        fat_n=''
        for r in fat_emesse:
            if r[3] == 'SIFIVA':
                f_sifiva +=r[2]
            if r[3] == 'GASNAZ':
                f_gasnaz +=r[2]
            if r[3] == 'BENNAZ':
                f_benznaz +=r[2]
            if r[3] == 'SIF':
                f_sif +=r[2]
            if r[3] == 'BENZ_8':
                f_benz8 +=r[2]
            if r[3] == '22':
                f_22 +=r[2]
            if r[1]:
                if r == fat_emesse[-1]: 
                    fat_n += r[1]
                else:    
                    fat_n += r[1] + '-'
                

        report = self.db.table('diporto.report').query(columns="""$data,$tot_gasolio, $tot_benzina""",
                                            where=where,
                                            data=data_report).fetch()
        
        vend_gasnaz=0
        vend_benznaz=0
        if report:
            vend_gasnaz = report[0][1]
            vend_benznaz = report[0][2]                       
        

        tot_giorn = f_sifiva + vend_benznaz + vend_gasnaz + f_sif + f_benz8 + f_22
        righe.append(dict(data=self.parameter('date'),doc_n=fat_n, sifiva=f_sifiva, gasnaz=vend_gasnaz,benznaz=vend_benznaz,sif=f_sif,benz8=f_benz8,a22=f_22,tot_estratto=tot_giorn))
        
        return righe    
    
    def calcRowHeight(self):
        #Determina l'altezza di ogni singola riga con approssimazione partendo dal valore di riferimento grid_row_height
        docn_offset = 20
        #Stabilisco un offset in termini di numero di caratteri oltre il quale stabilirò di andare a capo.
        #Attenzione che in questo caso ho una dimensione in num. di caratteri, mentre la larghezza della colonna è definita
        #in mm, e non avendo utti i caratteri la stessa dimensione si tratterà quindi di individuare la migliore approssimazione
          
        n_rows_docn = len(self.rowField('doc_n'))//docn_offset

      
  #      n_rows_nome_provincia = len(self.rowField('_sigla_provincia_nome'))//nome_offset + 1
        #In caso di valori in relazione, è necessario utilizzare "_" nel metodo rowField per recuperare correttamente i valori
        #A tal proposito si consiglia comunque sempre di utilizzare le aliasColumns
        #n_rows = max(n_rows_docn)#, n_rows_nome_provincia)
        height = (self.grid_row_height * n_rows_docn)
        return height
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
        if ext and not ext[0] == '.':
            ext = '.%s' % ext
        data=self.parameter('date').strftime("%d-%m-%Y")    
        doc_name = 'Estratto_giornaliero_{data}{ext}'.format(data=data, ext=ext)
        return doc_name

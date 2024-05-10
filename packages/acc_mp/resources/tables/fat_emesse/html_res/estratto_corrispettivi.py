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
    grid_header_height = 5
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

    def gridStruct(self,struct):
        #Questo metodo definisce la struttura della griglia di stampa definendone colonne e layout
        r = struct.view().rows()
        
        r.cell('data', mm_width=15, name='Data')
         #r.fieldcell('mese_fattura', hidden=True, subtotal='Totale {breaker_value}', subtotal_order_by="$data")
         #Questa formulaColumn verrà utilizzata per creare i subtotali per mese
        r.cell('doc_n', mm_width=0, name='Fattura n.')
        #r.cell('doc_n', hidden=True, subtotal='Totale documento {breaker_value}',subtotal_order_by='$cliente')
        r.cell('sifiva', mm_width=30, name='Olio Naz./Sif+Iva/Bunker', totalize=True,format='#,###.00')
        r.cell('gasnaz', mm_width=20, name='Gasolio Naz.', totalize=True,format='#,###.00')
        r.cell('benznaz', mm_width=20, name='Benzina Naz.', totalize=True,format='#,###.00')
        r.cell('sif', mm_width=20, name='Prodotto SIF', totalize=True,format='#,###.00')
        r.cell('benz8', mm_width=20, name='Benzina senza IVA', totalize=True,format='#,###.00')
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
            if r[1]:
                fat_n += r[1] + '-'    

        report = self.db.table('diporto.report').query(columns="""$data,$venduto_gas, $venduto_benz""",
                                            where=where,
                                            data=data_report).fetch()
        
        vend_gasnaz=0
        vend_benznaz=0
        if report:
            vend_gasnaz = report[0][1]
            vend_benznaz = report[0][2]                       
        

        tot_giorn = f_sifiva + vend_benznaz + vend_gasnaz + f_sif + f_benz8
        righe.append(dict(data=self.parameter('date'),doc_n=fat_n, sifiva=f_sifiva, gasnaz=vend_gasnaz,benznaz=vend_benznaz,sif=f_sif,benz8=f_benz8,tot_estratto=tot_giorn))
        #print(x)    
            #print(x)

        #for r in range(len(fat_emesse)):
        #    fat_id=fat_emesse[r][7]
        #    data_fat=fat_emesse[r][1]
        #    doc_n=fat_emesse[r][2]
        #    nome_imb=fat_emesse[r][3]
        #    importo_fat=fat_emesse[r][4]
        #    tot_pag=fat_emesse[r][5]
        #    saldo=fat_emesse[r][6]
        #    #insda=fat_emesse[r][7]
        #    #if insda == True:
        #    #    insda = 'x'
        #    #    saldo_fat = 0
        #    #else:
        #    #    insda = ''
        #    saldo_fat=importo_fat#
        #    pag_progressivo=0#
        #    for p in range(len(pagfatEmesse)):#
        #        if pagfatEmesse[p][0] == fat_id:
        #            data=pagfatEmesse[p][1]
        #            tot_pag=pagfatEmesse[p][2]
        #            descrizione_vers=pagfatEmesse[p][3]
        #            if nome_imb is not None:
        #                descrizione_vers='Importo versato - ' + str(nome_imb)
        #            else:
        #                descrizione_vers='Importo versato'   
        #            
        #            pag_progressivo += tot_pag
        #            saldo_fat = 0
        #            saldo_fat = importo_fat-pag_progressivo
        #            #
        #            righe_pag.append(dict(data=data,doc_n=doc_n, nome_imb=descrizione_vers, importo='',
        #                      tot_pag=tot_pag,saldo='',cliente=cliente))
        #    bal_cliente+=saldo_fat#
        #    #if r == len(fat_emesse)-1:
        #    #    righe_pag.append(dict(data='',doc_n='Balance', descrizione='Totale ' + str(cliente), importo='',
        #    #                  tot_pag='',saldo='',cliente='',balance_cliente=bal_cliente))    #
        #    righe_fat.append(dict(data=data_fat,doc_n=doc_n, nome_imb=nome_imb, importo=importo_fat,
        #                      tot_pag='',saldo=saldo_fat,cliente=cliente))
        #    
        #    righe = []
        #    righe_fat.extend(righe_pag)
        #    for myDict in righe_fat:
        #        if myDict not in righe:
        #            righe.append(myDict)
                
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
        if ext and not ext[0] == '.':
            ext = '.%s' % ext
        data=self.parameter('date').strftime("%d-%m-%Y")    
        doc_name = 'Estratto_giornaliero_{data}{ext}'.format(data=data, ext=ext)
        return doc_name

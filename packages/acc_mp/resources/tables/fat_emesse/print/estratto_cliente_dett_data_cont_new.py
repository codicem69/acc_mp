from datetime import datetime
from gnr.web.batch.btcprint import BaseResourcePrint
from gnr.core.gnrdecorator import public_method
import time
caption = 'Estratto dettaglio pagamenti in data new version'

class Main(BaseResourcePrint):
    batch_title = 'Estratto dettaglio pagamenti in data new version'
    batch_immediate='print'
    #Con batch_immediate='print' viene immediatamente aperta la stampa alla conclusione
    html_res = 'html_res/estratto_dettaglio_cliente_data_cont_new'
    #Questo parametro indica la risorsa di stampa da utilizzare

    def table_script_parameters_pane(self, pane,**kwargs):
       #Questo metodo consente l'inserimento di alcuni parametri da utilizzare per la stampa
        current_year = datetime.today().year

        years=''
        for r in range(20):
           years += ',' + (str(current_year-r))
       #last_years = [current_year, current_year-1, current_year-2, current_year-3, current_year-4]
       #years = ','.join(str(e) for e in last_years)
       #Prepariamo la stringa con gli ultimi 5 anni separati da virgola da passare alla filteringSelect
        fb = pane.formbuilder(cols=1, width='220px')
        #fb.div("Se la stampa al primo avvio non parte bisogna ripetere l'operazione")
        fb.checkbox(value='^.balance', label='!![it]Solo crediti', lbl='Balance', default=True)
        fb.div("Attenzione selezionando l'Anno verranno calcolati solo le fatture e pagamenti relativi a quell'Anno")
        fb.filteringSelect(value='^.anno', values=years, lbl='!![it]Anno', hidden='^.dal',validate_onAccept='FIRE #FORM.anno')
        fb.dateTextBox(value='^.dal',lbl='!![it]Data dal',period_to='.al',validate_notnull='^.al', hidden='^.anno')
        fb.dateTextBox(value='^.al',lbl='!![it]Data al',validate_notnull='^.dal', hidden='^.anno')
        fb.div("Se si vuole stampare la situazione di tutti i clienti non selezionare il cliente")
        fb.dbselect(value='^.cliente_id', table='acc_mp.cliente', lbl='Cliente', selected_rag_sociale='.rag_sociale',hasDownArrow=True)
        #fb.data('^.al',serverpath='data_saldo',dbenv=True) #passiamo nella env la data_saldo per essere utilizzata dalla formulaColumn nel calcolo del saldo alla data
       
        #fb.dataController("""if(anno){var txt_1=anno;
        #                    var txt_2 = '-12-31';
        #                    var result = txt_1.concat(txt_2);
        #                    var newdate=new Date(Date.parse(result));console.log(SET.datasaldo, typeof SET.datasaldo);
        #                    SET .datasaldo=newdate;}
        #                    else if(al) {SET .datasaldo=al;}
        #                    """,anno='^.anno', al='^.al')
        #fb.data('^.datasaldo',serverpath='data_saldo',dbenv=True, dtype='D')
        #fb.div('Nel caso di stampe per intero anno è preferibile selezionare solo crediti')
        
        #fb.dbselect(value='^.imbarcazione_id', table='acc_mp.imbarcazione', lbl='Imbarcazione', selected_nome='.nome',hasDownArrow=True,condition="$cliente_id=:cod",condition_cod='^.cliente_id')   
        #print(X)
    
    def pre_process(self):
        #passiamo nella env la data_saldo per essere utilizzata dalla formulaColumn nel calcolo del saldo alla data
        if self.batch_parameters['anno']:
            data = datetime.strptime(self.batch_parameters['anno'] + '-12-31', '%Y-%m-%d')
            self.page.pageStore().setItem('data_saldo',data)
            #time.sleep(5)
        if self.batch_parameters['al']:
            self.page.pageStore().setItem('data_saldo',self.batch_parameters['al'])
    
    

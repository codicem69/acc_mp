from datetime import datetime
from gnr.web.batch.btcprint import BaseResourcePrint

caption = 'Estratto Clienti dettaglio pag.'

class Main(BaseResourcePrint):
    batch_title = 'Estratto Clienti dettaglio pag.'
    batch_immediate='print'
    #Con batch_immediate='print' viene immediatamente aperta la stampa alla conclusione
    html_res = 'html_res/estratto_dettaglio_cliente'
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
       fb.checkbox(value='^.balance', label='!![it]Solo crediti', lbl='Balance')
       fb.div("Attenzione selezionando l'Anno verranno calcolati solo le fatture e pagamenti relativi a quell'Anno")
       fb.filteringSelect(value='^.anno', values=years, lbl='!![it]Anno', hidden='^.al')
       fb.dateTextBox(value='^.dal',lbl='!![it]Data dal',period_to='.al',validate_notnull='^.al', hidden='^.anno')
       fb.dateTextBox(value='^.al',lbl='!![it]Data al',validate_notnull='^.dal', hidden='^.anno')
       fb.dbselect(value='^.cliente_id', table='acc_mp.cliente', lbl='Cliente', selected_rag_sociale='.rag_sociale',hasDownArrow=True)
       #fb.data('^.al',serverpath='data_saldo',dbenv=True)#passiamo nella env la data_saldo per essere utilizzata dalla formulaColumn nel calcolo del saldo alla data
       #fb.dbselect(value='^.imbarcazione_id', table='acc_mp.imbarcazione', lbl='Imbarcazione', selected_nome='.nome',hasDownArrow=True,condition="$cliente_id=:cod",condition_cod='^.cliente_id')
   
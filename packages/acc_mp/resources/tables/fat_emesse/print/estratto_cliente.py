from datetime import datetime
from gnr.web.batch.btcprint import BaseResourcePrint

caption = 'Estratto Clienti'

class Main(BaseResourcePrint):
    batch_title = 'Estratto Clienti'
    batch_immediate='print'
    #Con batch_immediate='print' viene immediatamente aperta la stampa alla conclusione
    html_res = 'html_res/estratto_cliente'
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
       fb.filteringSelect(value='^.anno', values=years, lbl='!![it]Anno')
       fb.dateTextBox(value='^.dal',lbl='!![it]Data dal',period_to='.al')
       fb.dateTextBox(value='^.al',lbl='!![it]Data al')
   #    fb.dbselect(value='^.cliente_id', table='fatt.cliente', lbl='Cliente', selected_ragione_sociale='.ragione_sociale')

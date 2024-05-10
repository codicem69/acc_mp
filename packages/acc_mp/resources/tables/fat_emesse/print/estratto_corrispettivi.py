from datetime import datetime
from gnr.web.batch.btcprint import BaseResourcePrint

caption = 'Estratto Corrispettivi'

class Main(BaseResourcePrint):
    batch_title = 'Estratto Corrispettivi'
    batch_immediate='print'
    #Con batch_immediate='print' viene immediatamente aperta la stampa alla conclusione
    html_res = 'html_res/estratto_corrispettivi'
    #Questo parametro indica la risorsa di stampa da utilizzare

    def table_script_parameters_pane(self, pane,**kwargs):
       #Questo metodo consente l'inserimento di alcuni parametri da utilizzare per la stampa

       fb = pane.formbuilder(cols=1, width='220px')
       fb.datetextbox(value='^.date', lbl='!![it]Data')

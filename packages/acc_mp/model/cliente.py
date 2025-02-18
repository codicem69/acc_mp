# encoding: utf-8

from gnr.core.gnrnumber import floatToDecimal,decimalRound

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('cliente', pkey='id', name_long='!![it]Cliente', name_plural='!![it]Cliente',caption_field='full_cliente')
        self.sysFields(tbl)

        tbl.column('rag_sociale', name_short='!![it]Ragione sociale')
        tbl.column('indirizzo', name_short='!![it]Indirizzo')
        tbl.column('cap', name_short='!![it]CAP')
        tbl.column('citta', name_short='!![it]Città')
        tbl.column('vat', name_short='!![it]P.IVA')
        tbl.column('cf', name_short='!![it]Codice fiscale')
        tbl.column('cod_univoco',size='7', name_short='!![it]Codice univoco')
        tbl.column('pec', name_short='Email pec')
        tbl.column('email', name_short='Email')
        tbl.column('tel', name_short='Tel.')
        tbl.column('note', name_short='Note')
        tbl.column('balance', dtype='N', name_short='!![it]Saldo contabile',format='#,###.00', batch_assign=True)
        tbl.formulaColumn('full_cliente',"""$rag_sociale || coalesce(' - '|| $indirizzo, '') || coalesce(' - '|| $cap,'') || coalesce(' - '|| $citta,'') || 
                          coalesce(' P.IVA: ' || $vat,'') || coalesce(' - codice univoco: ' || $cod_univoco,'') || coalesce(' - pec: ' || $pec,'') """ )
        #tbl.formulaColumn('tot_pag',select=dict(table='acc_mp.pag_fat_emesse',columns='coalesce(sum($importo),0)', where='@fatt_emesse_id.cliente_id=#THIS.id'),dtype='N',format='#,###.00',
        #                  name_long='!![it]Totale pagamenti')
                                  
    def ricalcolaBalanceCliente(self,cliente_id=None):
        with self.recordToUpdate(cliente_id) as record:
            totale_fatture = self.db.table('acc_mp.fat_emesse').readColumns(columns="""SUM($importo) AS totale_fatture""",
                                                                     where='$cliente_id=:c_id',c_id=cliente_id)
            fatture_cliente_id = self.db.table('acc_mp.fat_emesse').query(columns='$id',where='$cliente_id=:c_id', c_id=cliente_id).fetchAsDict('id')
            totale_pagato = 0
           
            for r in fatture_cliente_id:
                pagamenti = self.db.table('acc_mp.pag_fat_emesse').query(columns='$importo',
                                                                     where='$fatt_emesse_id=:fe_id', fe_id=r).fetch()
                for a in range(len(pagamenti)):
                    totale_pagato += pagamenti[a][0]
           
            if totale_fatture is None:
                record['balance'] = None
            else:    
                record['balance'] = floatToDecimal(totale_fatture - totale_pagato or 0)
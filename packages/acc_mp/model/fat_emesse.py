# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('fat_emesse', pkey='id', name_long='!![it]Fattura emessa', name_plural='!![it]Fatture emesse',caption_field='doc_imp')
        self.sysFields(tbl)
        
        tbl.column('cliente_id',size='22', group='_', name_long='cliente_id',batch_assign=True
                    ).relation('cliente.id', relation_name='fatt_cliente', mode='foreignkey', onDelete='raise')
        tbl.column('imbarcazione_id',size='22', group='_', name_long='imbarcazione_id',batch_assign=True
                    ).relation('imbarcazione.id', relation_name='fatt_imb', mode='foreignkey', onDelete='raise')
        tbl.column('data', dtype='D', name_short='!![it]Data')
        tbl.column('doc_n', name_short='!![it]Doc.no.', dtype='T')
        tbl.column('importo', dtype='money', name_short='!![it]Importo')
        tbl.column('scadenza', dtype='D', name_short='!![it]Scadenza')
        tbl.column('tip_vend',size=':6', group='_', name_long='!![it]Tipologia venduto'
                    ).relation('tipologia_venduto.code', relation_name='tip_venduto', mode='foreignkey', onDelete='raise')
        tbl.column('note', name_short='!![it]Note')
        tbl.formulaColumn('giorni_scadenza',"""CASE WHEN ($scadenza - CURRENT_DATE)>0 AND $saldo>0 THEN 'Scadenza tra giorni ' || cast(($scadenza - CURRENT_DATE) as varchar)
                                        WHEN ($scadenza - CURRENT_DATE)>0 AND $saldo<=0  THEN '!![en]PAYED' 
                                        WHEN ($scadenza - CURRENT_DATE)<0 AND $saldo<=0 THEN '!![en]PAYED' ELSE 'Scaduta da giorni ' || cast((CURRENT_DATE-$scadenza) as varchar) END """,
                                        name_long='!![en]Expire days', dtype='T')
        #tbl.formulaColumn('tot_pag',select=dict(table='acc_mp.pag_fat_emesse',columns='coalesce(SUM($importo),0)', where="$fatt_emesse_id=#THIS.id"),dtype='N',format='#,###.00',
        #                  name_long='!![it]Totale pagato')

        #formulaColumn parametrica prelevando la data di calcolo dal dbEnv fissato nella th della toolbar: 
        # bar.data('^acc_mp_fat_emesse.view.queryBySample.c_0',serverpath='data_saldo',dbenv=True)
        tbl.formulaColumn('tot_pag',select=dict(table='acc_mp.pag_fat_emesse', columns='coalesce(SUM($importo),0)', 
                                                where='$fatt_emesse_id=#THIS.id AND $data<=coalesce(:env_data_saldo,:env_workdate)'))#, var_data_rif='2024-12-31')
        tbl.formulaColumn('tot_pag_effettivo',select=dict(table='acc_mp.pag_fat_emesse', columns='coalesce(SUM($importo),0)', 
                                                where='$fatt_emesse_id=#THIS.id'))
        tbl.formulaColumn('saldo_effettivo', "$importo-coalesce($tot_pag_effettivo,0)",dtype='N',name_long='!![it]Saldo Effettivo',format='#,###.00')
        tbl.formulaColumn('saldo', "$importo-coalesce($tot_pag,0)",dtype='N',name_long='!![it]Saldo',format='#,###.00')
        tbl.formulaColumn('semaforo_eff',"""CASE WHEN $saldo_effettivo = 0 THEN true ELSE false END""",dtype='B',name_long=' ')
        tbl.formulaColumn('semaforo_al',"""CASE WHEN $saldo = 0 THEN true ELSE false END""",dtype='B',name_long=' ')
        tbl.formulaColumn('anno_doc',"date_part('year', $data)", dtype='D')
        tbl.formulaColumn('doc_imp',"$doc_n || ' € ' || $importo || ' - ' || $note")

    def aggiornaCliente(self,record):
        cliente_id = record['cliente_id']
        self.db.deferToCommit(self.db.table('acc_mp.cliente').ricalcolaBalanceCliente,
                                    cliente_id=cliente_id,
                                    _deferredId=cliente_id)

    def trigger_onInserted(self,record=None):
        self.aggiornaCliente(record)

    def trigger_onUpdated(self,record=None,old_record=None):
        self.aggiornaCliente(record)

    def trigger_onDeleted(self,record=None):
        if self.currentTrigger.parent:
            return
        self.aggiornaCliente(record)
        

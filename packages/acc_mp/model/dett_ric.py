# encoding: utf-8


class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('dett_ric',pkey='id',name_long='dett_ric',name_plural='dett_ric',caption_field='id')
        self.sysFields(tbl)
        tbl.column('ric_id',size='22',name_long='ric_id',name_short='ric_id').relation('ricevuta.id',relation_name='dett_ric_id', mode='foreignkey', onDelete='cascade')
        tbl.column('prod_id',size='22',name_long='prodotto id',name_short='prod_id').relation('diporto.prodotti.id',relation_name='dett_ric_prod_id', mode='foreignkey', onDelete='raise')
        tbl.column('quantita',dtype='N',size='10,2',name_long='quantità',name_short='quantita',format='#,###.00')
        tbl.column('prezzo_un',dtype='N',size='10,3',name_long='prezzo unitario',name_short='prezzo_un',format='#,###.000')
        tbl.column('totale',dtype='N',size='10,2',name_long='totale',name_short='tot',format='#,###.00')

    def ricalcolaTotali(self,record):
            ric_id = record['ric_id']
            self.db.deferToCommit(self.db.table('acc_mp.ricevuta').ricalcolaTotali,
                                    ric_id=ric_id,
                                    _deferredId=ric_id)
    
    def trigger_onInserted(self,record=None):
        self.ricalcolaTotali(record)

    def trigger_onUpdated(self,record=None,old_record=None):
        self.ricalcolaTotali(record)
        
    def trigger_onDeleted(self,record=None):
        if self.currentTrigger.parent:
            return
        self.ricalcolaTotali(record)

# encoding: utf-8
# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('estratto_dettagli', pkey='id', name_long='!![it]Dettaglio Estratto corrispettivi', name_plural='!![it]Dettaglio Estratti corrispettivi',caption_field='id')
        self.sysFields(tbl)
        tbl.column('estratto_id',size='22', group='_', name_long='!![it]Estratto id'
                    ).relation('estratto_corrisp.id', relation_name='estratto_righe', mode='foreignkey', onDelete='cascade')
        tbl.column('fattura_id',size='22', group='_', name_long='!![it]Fattura n.'
                    ).relation('fat_emesse.id', relation_name='fatture_emesse', mode='foreignkey', onDelete='raise')
        tbl.column('sifiva', dtype='money', name_short='!![it]Olio Naz. / Sif+IVA / Bunker')
        tbl.column('gasiva', dtype='money', name_short='!![it]Gasolio Naz.')
        tbl.column('benziva', dtype='money', name_short='!![it]Benzina Naz.')
        tbl.column('sif', dtype='money', name_short='!![it]SIF')
        tbl.column('benz_8', dtype='money', name_short='!![it]Benzina S/IVA')
        tbl.column('note', name_short='!![it]Note')
        
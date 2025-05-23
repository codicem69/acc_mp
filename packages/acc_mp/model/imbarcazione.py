# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('imbarcazione', pkey='id', name_long='!![it]Imbarcazione', name_plural='!![it]Imbarcazioni',caption_field='nome')
        self.sysFields(tbl)
        tbl.column('cliente_id',size='22', group='_', name_long='!![it]Cliente id'
                    ).relation('cliente.id', relation_name='cliente_imb', mode='foreignkey', onDelete='raise')
        tbl.column('tip_id',size=':3', group='_', name_long='!![it]Tipologia'
                    ).relation('tipologia_imb.code', relation_name='tip_imb', mode='foreignkey', onDelete='raise')
        tbl.column('nome', name_short='!![it]Nome')
        tbl.column('reg_n', name_short='!![en]Numero reg.')
        tbl.formulaColumn('full_imb',"$nome || coalesce(' - ' || reg_n,'') || ' - ' || @cliente_id.rag_sociale || coalesce(' - PIVA ' || @cliente_id.vat,'')")
        
# encoding: utf-8

from gnr.core.gnrdecorator import metadata

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('tipologia_imb', pkey='code', name_long='!![it]Tipologia imbarcazione', name_plural='!![it]Tipologia imbarcazioni',
                                            caption_field='descrizione',lookup=True)
        self.sysFields(tbl,id=False)
        tbl.column('code',size=':3',name_long='!![it]Codifica')
        tbl.column('descrizione', name_short='!![it]Descrizione')

    @metadata(mandatory=True)
    def sysRecord_MP(self):
        return self.newrecord(code='MP', descrizione='M/P')

    @metadata(mandatory=True)
    def sysRecord_MY(self):
        return self.newrecord(code='MY', descrizione='M/Y')

    @metadata(mandatory=True)
    def sysRecord_MN(self):
        return self.newrecord(code='MN', descrizione='M/N')

    @metadata(mandatory=True)
    def sysRecord_MB(self):
        return self.newrecord(code='MB', descrizione='M/B')

    @metadata(mandatory=True)
    def sysRecord_MV(self):
        return self.newrecord(code='MV', descrizione='M/V')

    @metadata(mandatory=True)
    def sysRecord_GM(self):
        return self.newrecord(code='GM', descrizione='GOM')

    @metadata(mandatory=True)
    def sysRecord_RE(self):
        return self.newrecord(code='RE', descrizione='R/RE')

    @metadata(mandatory=True)
    def sysRecord_MPN(self):
        return self.newrecord(code='MPN', descrizione='M/PNE')

    @metadata(mandatory=True)
    def sysRecord_HSC(self):
        return self.newrecord(code='HSC', descrizione='HSC')

    @metadata(mandatory=True)
    def sysRecord_AFO(self):
        return self.newrecord(code='AFO', descrizione='A/FO')

    @metadata(mandatory=True)
    def sysRecord_GTE(self):
        return self.newrecord(code='GTE', descrizione='G/TE')    
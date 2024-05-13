# encoding: utf-8
class Menu(object):
    def config(self,root,**kwargs):
        taguser = self.db.currentEnv.get('userTags')
        tag_user=taguser.split(',')

        if 'admin' in tag_user or 'superadmin' in tag_user or '_DEV_' in tag_user:
            root.packageBranch('Contabilità carburanti',pkg='acc_mp')
            root.packageBranch('Amministrazione sistema',pkg='adm')
            root.packageBranch('System',pkg='sys')

        else:
            root.thpage(u"!![it]Cliente", table="acc_mp.cliente", multipage="True", tags="")
            root.thpage(u"fat_emesse", table="acc_mp.fat_emesse", multipage="True", tags="")
            root.thpage(u"!![it]Imbarcazioni", table="acc_mp.imbarcazione", multipage="True", tags="")
            #root.thpage(u"!![it]Pagamenti", table="acc_mp.pag_fat_emesse", multipage="True", tags="")
            #root.thpage(u"!![it]Estratto per corrispettivi", table="acc_mp.estratto_corrisp", multipage="True", tags="")
            root.lookupBranch(u"Lookup tables", pkg="acc_mp")

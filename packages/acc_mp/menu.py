# encoding: utf-8
class Menu(object):
    def config(self,root,**kwargs):
        user=self.db.currentEnv.get('user')
        taguser = self.db.currentEnv.get('userTags')
        tag_user=taguser.split(',')
        if 'admin' in tag_user or 'superadmin' in tag_user or '_DEV_' in tag_user:
            accmp = root.branch(u"acc_mp", tags="")
            accmp.packageBranch('Amministrazione sistema',pkg='adm')#, branchMethod='userSubmenu')
            accmp.packageBranch('System',pkg='sys')
            accmp.packageBranch('Agencies',pkg='agz')
            accmp.thpage(u"!![it]Cliente", table="acc_mp.cliente", multipage="True", tags="")
            accmp.thpage(u"fat_emesse", table="acc_mp.fat_emesse", multipage="True", tags="")
            accmp.thpage(u"!![it]Imbarcazioni", table="acc_mp.imbarcazione", multipage="True", tags="")
            accmp.thpage(u"!![it]Pagamenti", table="acc_mp.pag_fat_emesse", multipage="True", tags="")
            accmp.thpage(u"!![it]Ricevuta", table="acc_mp.ricevuta", multipage="True", tags="")
            accmp.lookupBranch(u"Lookup tables", pkg="acc_mp")
        else:
            #accmp = root.branch(u"acc_mp", tags="")
            root.thpage(u"!![it]Cliente", table="acc_mp.cliente", multipage="True", tags="")
            root.thpage(u"fat_emesse", table="acc_mp.fat_emesse", multipage="True", tags="")
            root.thpage(u"!![it]Imbarcazioni", table="acc_mp.imbarcazione", multipage="True", tags="")
            root.thpage(u"!![it]Ricevuta", table="acc_mp.ricevuta", multipage="True", tags="")
            #accmp.thpage(u"!![it]Pagamenti", table="acc_mp.pag_fat_emesse", multipage="True", tags="")
            root.lookupBranch(u"Lookup tables", pkg="acc_mp")

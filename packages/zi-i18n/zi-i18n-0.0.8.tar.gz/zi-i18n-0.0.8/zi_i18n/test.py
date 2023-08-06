from zi_i18n import I18n

i18n = I18n()
i18n.translate("example.text")
print(i18n.cache)
print(i18n.translate("example.text"))
i18n.change_lang("id_ID", clear_cache=True)
print(i18n.cache)

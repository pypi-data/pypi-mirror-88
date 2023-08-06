# zi-i18n
A Experimental Internationalization

example:

Translation
```python
#in "example.py" file
from zi_i18n import I18n

i18n = I18n("locale", "en_US")
print(i18n.translate("example.text"))

#in "locale/en_US.zi.lang" file
<!example.text: "Test">
#output: Test
```

Pluralization
```python
#in "example.py" file
from zi_i18n import I18n

i18n = I18n("locale", "en_US")
print(i18n.translate("example.plural", count=0))
print(i18n.translate("example.plural", count=1))
print(i18n.translate("example.plural", count=5))

#in "locale/en_US.zi.lang" file
<%example.plural: {"zero": "0", "one": "1", "many": ">= 2"}
#output:
# 0
# 1
# >= 2
```

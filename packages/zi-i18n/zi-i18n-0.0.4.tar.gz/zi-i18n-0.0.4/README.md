# zi-i18n
A Experimental Internationalization

example:

```python
#in "example.py" file
from zi_i18n import I18n

i18n = I18n("locale", "en_US")
print(i18n.translate("example.text"))

#in "locale/en_US.zi.lang" file
<!example.text: "Test">
#output: Test
```

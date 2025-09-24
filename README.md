![](clinkey_preview.png)  

---
```bash
Your password generator *'buddy'*, available on a CLI.  
```
---
```bash
Usage python3 heat.py clinkey [OPTIONS]
```
---
```bash
-l, --length				The desired length for the output password(s)
-n, --number				The amount of password you are expecting from ClinKey to generate.
-o, --output				The path of a file in which to print the result instead of echoing it into the Terminal.
-t --type					The strength and complexity of the password content. 
								Possible values:
									- 'normal' - Containing only alphabetical characters.
									- 'strong' - Mixing letters and digits.
									- 'super_strong' - Adding special characters to the result.
-ns, --no-sep				Clear the result from the hyphens used to separate the groups of letters usually forming the result.
-low, --lower				Transform the output password in lowercase string.

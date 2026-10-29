# Max opcodes getter
Этот скрипт:
1. Скрапит `rustore` и получает актальную версию max
2. Скачивает apk и отдаёт его `jadx`
3. Находит opcode`ы и выводит их в том порядке как они занумерованы в коде max. Там они пишутся так(например):
```java
f80850J3 = new vld("NOTIF_BANNERS", 170, 292);
```
как несложно заметить здесь третье число(292) это opcode а второе(170) - я решил что порядковый номер


> [!WARNING]
> Для того чтоб оно работало надо чтоб был установлен `jadx`
> ```bash
> sudo pacman -S jadx
> ```

## Disclaimer
### No Affiliation
This project is an independent, unofficial, third-party tool and is provided for educational and research purposes only.
The author of this project is NOT affiliated with, associated with, authorized by, endorsed by, sponsored by, or in any way officially connected with:
- MAX messenger (JSC "VK", the "MAX" application, ru.oneme.app, and its developers, owners, and operators),
- VK (VK Company / JSC "VK" and all of its subsidiaries, services, products, and affiliates),
- RuStore (and its operators, owners, and affiliates),

or any of their respective subsidiaries, parent companies, partners, developers, employees, agents, or licensors. All product names, trademarks, brands, logos, and copyrights mentioned or used in this project are the property of their respective owners. Their use in this project does not imply any endorsement, partnership, or affiliation, and the author makes no claim of affiliation or representation of any of the above parties.
### Legal Risks & Terms of Service
Running this script — which downloads an application from a third-party source, decompiles it, and extracts data from its code — may violate the Terms of Service / End User License Agreements of MAX, VK, RuStore, or any other party, and may be illegal in your country or jurisdiction (including, without limitation, violations of copyright law, anti-circumvention / DMCA-style legislation, computer fraud and abuse laws, or other applicable local, national, or international laws).
You are solely responsible for determining whether your use of this script is lawful and permitted in your jurisdiction and under any applicable agreements. It is your responsibility to read and comply with the relevant Terms of Service before using this tool. The author does not encourage, promote, or condone any illegal activity or breach of any agreement.
### No Warranty — "AS IS"
This software is provided "AS IS", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, accuracy, correctness, completeness, and non-infringement.
The script may:
- produce incorrect, incomplete, inaccurate, or outdated results,
- fail entirely or stop working at any time (e.g., due to changes in the app, CDN, RuStore, or other external dependencies),
- behave unpredictably.
### Limitation of Liability
In no event shall the author or copyright holder be liable for any claim, damages, or other liability — whether in an action of contract, tort, or otherwise — arising from, out of, or in connection with the use of (or inability to use) this script, including but not limited to:
- any legal consequences of any kind (civil, administrative, or criminal liability, fines, penalties, prosecution, account bans, or blocks),
- any harm to your hardware, software, data, or network (including data loss, device damage, or malfunction),
- any financial, reputational, or other losses of any kind,
- any indirect, incidental, special, consequential, or punitive damages.

By using this script, you acknowledge that you have read, understood, and accepted this disclaimer in full, and you do so entirely at your own risk. If you do not agree with any part of this disclaimer, do not use this script.

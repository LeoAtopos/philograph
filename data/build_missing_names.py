"""
Add missing philosopher name translations to i18n-data.js
"""
import json, re

with open('data/philosophers.json', 'r', encoding='utf-8') as f:
    western = json.load(f)
with open('data/chinese-philosophers.json', 'r', encoding='utf-8') as f:
    chinese = json.load(f)

with open('js/i18n-data.js', 'r', encoding='utf-8') as f:
    content = f.read()

name_start = content.index("  name: {")
name_end = content.index('  },', name_start + 10)
name_section = content[name_start:name_end]
existing_names = set(re.findall(r"'([^']+)'\s*:", name_section))

ZH_NAMES = {
    'arendt': 'Hannah Arendt',
    'berkeley': 'George Berkeley',
    'chenghao': 'Cheng Hao',
    'daizhen': 'Dai Zhen',
    'davidson': 'Donald Davidson',
    'derrida': 'Jacques Derrida',
    'dewey': 'John Dewey',
    'fazang': 'Fazang',
    'foucault': 'Michel Foucault',
    'gongsunlong': 'Gongsun Long',
    'gongzizhen': 'Gong Zizhen',
    'guoxiang': 'Guo Xiang',
    'habermas': 'Jurgen Habermas',
    'heraclitus': 'Heraclitus',
    'hobbes': 'Thomas Hobbes',
    'huineng': 'Huineng',
    'husserl': 'Edmund Husserl',
    'james': 'William James',
    'jikang': 'Ji Kang',
    'kangyouwei': 'Kang Youwei',
    'kierkegaard': 'Soren Kierkegaard',
    'laosiguang': 'Lao Siguang',
    'li_zhi': 'Li Zhi',
    'liangqichao': 'Liang Qichao',
    'liangshuming': 'Liang Shuming',
    'liezi': 'Liezi',
    'liuzongyuan': 'Liu Zongyuan',
    'lu_jiuyuan': 'Lu Jiuyuan',
    'merleau-ponty': 'Maurice Merleau-Ponty',
    'montesquieu': 'Montesquieu',
    'nozick': 'Robert Nozick',
    'ockham': 'William of Ockham',
    'parmenides': 'Parmenides',
    'pascal': 'Blaise Pascal',
    'peirce': 'Charles Sanders Peirce',
    'plotinus': 'Plotinus',
    'qianmu': 'Qian Mu',
    'quine': 'W.V.O. Quine',
    'schopenhauer': 'Arthur Schopenhauer',
    'searle': 'John Searle',
    'shen_buhai': 'Shen Buhai',
    'singer': 'Peter Singer',
    'sunzi': 'Sun Tzu',
    'tangjunyi': 'Tang Junyi',
    'wangbi': 'Wang Bi',
    'weiyuan': 'Wei Yuan',
    'xiongshili': 'Xiong Shili',
    'xuanzang': 'Xuanzang',
    'yangxiong': 'Yang Xiong',
    'zhangtaiyan': 'Zhang Taiyan',
    'zhangzai': 'Zhang Zai',
    'zhiyi': 'Zhiyi',
    'zhou_dunyi': 'Zhou Dunyi',
    'zouyan': 'Zou Yan',
}

# These are name entries: string format { en: 'name', zh: 'name' }
# For western philosophers, en = english name, zh = chinese name
# For chinese philosophers, en = pinyin/english name, zh = chinese name
ZH_NAMES_ZH = {
    'arendt': { 'en': 'Hannah Arendt', 'zh': '汉娜·阿伦特' },
    'berkeley': { 'en': 'George Berkeley', 'zh': '乔治·贝克莱' },
    'chenghao': { 'en': 'Cheng Hao', 'zh': '程颢' },
    'daizhen': { 'en': 'Dai Zhen', 'zh': '戴震' },
    'davidson': { 'en': 'Donald Davidson', 'zh': '唐纳德·戴维森' },
    'derrida': { 'en': 'Jacques Derrida', 'zh': '雅克·德里达' },
    'dewey': { 'en': 'John Dewey', 'zh': '约翰·杜威' },
    'fazang': { 'en': 'Fazang', 'zh': '法藏' },
    'foucault': { 'en': 'Michel Foucault', 'zh': '米歇尔·福柯' },
    'gongsunlong': { 'en': 'Gongsun Long', 'zh': '公孙龙' },
    'gongzizhen': { 'en': 'Gong Zizhen', 'zh': '龚自珍' },
    'guoxiang': { 'en': 'Guo Xiang', 'zh': '郭象' },
    'habermas': { 'en': 'Jurgen Habermas', 'zh': '尤尔根·哈贝马斯' },
    'heraclitus': { 'en': 'Heraclitus', 'zh': '赫拉克利特' },
    'hobbes': { 'en': 'Thomas Hobbes', 'zh': '托马斯·霍布斯' },
    'huineng': { 'en': 'Huineng', 'zh': '惠能' },
    'husserl': { 'en': 'Edmund Husserl', 'zh': '埃德蒙德·胡塞尔' },
    'james': { 'en': 'William James', 'zh': '威廉·詹姆斯' },
    'jikang': { 'en': 'Ji Kang', 'zh': '嵇康' },
    'kangyouwei': { 'en': 'Kang Youwei', 'zh': '康有为' },
    'kierkegaard': { 'en': 'Soren Kierkegaard', 'zh': '索伦·克尔凯郭尔' },
    'laosiguang': { 'en': 'Lao Siguang', 'zh': '劳思光' },
    'li_zhi': { 'en': 'Li Zhi', 'zh': '李贽' },
    'liangqichao': { 'en': 'Liang Qichao', 'zh': '梁启超' },
    'liangshuming': { 'en': 'Liang Shuming', 'zh': '梁漱溟' },
    'liezi': { 'en': 'Liezi', 'zh': '列子' },
    'liuzongyuan': { 'en': 'Liu Zongyuan', 'zh': '柳宗元' },
    'lu_jiuyuan': { 'en': 'Lu Jiuyuan', 'zh': '陆九渊' },
    'merleau-ponty': { 'en': 'Maurice Merleau-Ponty', 'zh': '莫里斯·梅洛-庞蒂' },
    'montesquieu': { 'en': 'Montesquieu', 'zh': '孟德斯鸠' },
    'nozick': { 'en': 'Robert Nozick', 'zh': '罗伯特·诺齐克' },
    'ockham': { 'en': 'William of Ockham', 'zh': '奥卡姆' },
    'parmenides': { 'en': 'Parmenides', 'zh': '巴门尼德' },
    'pascal': { 'en': 'Blaise Pascal', 'zh': '布莱兹·帕斯卡' },
    'peirce': { 'en': 'Charles Sanders Peirce', 'zh': '查尔斯·桑德斯·皮尔士' },
    'plotinus': { 'en': 'Plotinus', 'zh': '普罗提诺' },
    'qianmu': { 'en': 'Qian Mu', 'zh': '钱穆' },
    'quine': { 'en': 'W.V.O. Quine', 'zh': 'W.V.O.蒯因' },
    'schopenhauer': { 'en': 'Arthur Schopenhauer', 'zh': '阿图尔·叔本华' },
    'searle': { 'en': 'John Searle', 'zh': '约翰·塞尔' },
    'shen_buhai': { 'en': 'Shen Buhai', 'zh': '申不害' },
    'singer': { 'en': 'Peter Singer', 'zh': '彼得·辛格' },
    'sunzi': { 'en': 'Sun Tzu', 'zh': '孙子' },
    'tangjunyi': { 'en': 'Tang Junyi', 'zh': '唐君毅' },
    'wangbi': { 'en': 'Wang Bi', 'zh': '王弼' },
    'weiyuan': { 'en': 'Wei Yuan', 'zh': '魏源' },
    'xiongshili': { 'en': 'Xiong Shili', 'zh': '熊十力' },
    'xuanzang': { 'en': 'Xuanzang', 'zh': '玄奘' },
    'yangxiong': { 'en': 'Yang Xiong', 'zh': '扬雄' },
    'zhangtaiyan': { 'en': 'Zhang Taiyan', 'zh': '章太炎' },
    'zhangzai': { 'en': 'Zhang Zai', 'zh': '张载' },
    'zhiyi': { 'en': 'Zhiyi', 'zh': '智顗' },
    'zhou_dunyi': { 'en': 'Zhou Dunyi', 'zh': '周敦颐' },
    'zouyan': { 'en': 'Zou Yan', 'zh': '邹衍' },
}

# Find missing names
all_phils = {}
for p in western + chinese:
    all_phils[p['id']] = p['name']

missing = []
for pid in sorted(all_phils.keys()):
    if pid not in existing_names:
        missing.append(pid)

lines = []
lines.append("    // === Newly added philosophers ===")
for pid in missing:
    if pid in ZH_NAMES_ZH:
        entry = ZH_NAMES_ZH[pid]
        lines.append(f"    '{pid}': {{ en: '{entry['en']}', zh: '{entry['zh']}' }},")
    else:
        name = all_phils[pid]
        safe = name.replace("\\", "\\\\").replace("'", "\\'")
        lines.append(f"    '{pid}': {{ en: '{safe}', zh: '{safe}' }},")

missing_text = '\n'.join(lines)

# Insert before closing of name section
new_content = content[:name_end] + '\n' + missing_text + '\n' + content[name_end:]

with open('js/i18n-data.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Added {len(missing)} name entries")

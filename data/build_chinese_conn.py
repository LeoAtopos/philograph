import json

connections = [
    # === 孔子 ↔ Laozi ===
    {"from": "kz1", "fromPhil": "kongzi", "to": "lz1", "toPhil": "laozi", "type": "N", "label": "Ren (benevolence) vs Dao: human virtue vs transcendent spontaneity"},
    {"from": "kz2", "fromPhil": "kongzi", "to": "lz2", "toPhil": "laozi", "type": "N", "label": "Ritual (Li) vs Non-action (Wu wei)"},
    {"from": "kz4", "fromPhil": "kongzi", "to": "lz5", "toPhil": "laozi", "type": "N", "label": "Rectification of names vs the unnameable Dao"},
    {"from": "lz6", "fromPhil": "laozi", "to": "kz3", "toPhil": "kongzi", "type": "N", "label": "Weakness overcomes strength vs the Junzi's active cultivation"},

    # === 孔子 ↔ Sunzi ===
    {"from": "kz10", "fromPhil": "kongzi", "to": "sz3", "toPhil": "sunzi", "type": "N", "label": "Virtue (De) attracts without force vs deception in warfare"},
    {"from": "sz2", "fromPhil": "sunzi", "to": "kz9", "toPhil": "kongzi", "type": "P", "label": "Self-knowledge is the foundation of strategy and virtue"},

    # === 孔子 ↔ Mozi ===
    {"from": "mo1", "fromPhil": "mozi", "to": "kz1", "toPhil": "kongzi", "type": "N", "label": "Love must be universal, not graded by relation"},
    {"from": "mo2", "fromPhil": "mozi", "to": "kz2", "toPhil": "kongzi", "type": "P", "label": "Ritual serves the people, not the other way around"},
    {"from": "mo5", "fromPhil": "mozi", "to": "kz2", "toPhil": "kongzi", "type": "N", "label": "Music is extravagant and should be abolished"},

    # === 孟子 ↔ 孔子 ===
    {"from": "mz1", "fromPhil": "mengzi", "to": "kz1", "toPhil": "kongzi", "type": "P", "label": "Extends Confucian benevolence as innate human nature"},
    {"from": "mz2", "fromPhil": "mengzi", "to": "kz3", "toPhil": "kongzi", "type": "P", "label": "Four sprouts develop the Junzi ideal"},
    {"from": "mz3", "fromPhil": "mengzi", "to": "kz4", "toPhil": "kongzi", "type": "P", "label": "People-centered governance refines Zhengming"},
    {"from": "mz5", "fromPhil": "mengzi", "to": "kz5", "toPhil": "kongzi", "type": "P", "label": "Vast flowing qi develops filial piety into cosmic moral energy"},
    {"from": "mz4", "fromPhil": "mengzi", "to": "kz10", "toPhil": "kongzi", "type": "P", "label": "Mandate of Heaven depends on virtue, not conquest"},

    # === 庄子 ↔ Laozi ===
    {"from": "zz1", "fromPhil": "zhuangzi", "to": "lz1", "toPhil": "laozi", "type": "P", "label": "Radicalizes Dao into spiritual freedom"},
    {"from": "zz2", "fromPhil": "zhuangzi", "to": "kz4", "toPhil": "kongzi", "type": "N", "label": "All distinctions are empty; names cannot capture truth"},
    {"from": "zz2", "fromPhil": "zhuangzi", "to": "mz1", "toPhil": "mengzi", "type": "N", "label": "Good and evil are relative; human nature transcends categories"},
    {"from": "zz6", "fromPhil": "zhuangzi", "to": "lz5", "toPhil": "laozi", "type": "P", "label": "Language as fish trap extends the unnameable Dao"},

    # === 庄子 ↔ Liezi ===
    {"from": "lzr1", "fromPhil": "liezi", "to": "zz1", "toPhil": "zhuangzi", "type": "P", "label": "Dao as spontaneity develops Zhuangzi's free wandering"},    {"from": "lzr2", "fromPhil": "liezi", "to": "zz4", "toPhil": "zhuangzi", "type": "P", "label": "Freedom from attachments extends the useless usefulness"},    {"from": "lzr3", "fromPhil": "liezi", "to": "zz2", "toPhil": "zhuangzi", "type": "P", "label": "Relativity of perspective develops equalizing all things"},    # === 荀子 ↔ 孔子, 孟子, 韩非 ===
    {"from": "xz1", "fromPhil": "xunzi", "to": "mz1", "toPhil": "mengzi", "type": "N", "label": "Human nature is evil, not good — goodness is artificial"},
    {"from": "xz2", "fromPhil": "xunzi", "to": "kz2", "toPhil": "kongzi", "type": "P", "label": "Ritual transforms selfish nature into morality"},
    {"from": "xz3", "fromPhil": "xunzi", "to": "ds2", "toPhil": "dongzhongshu", "type": "N", "label": "Heaven has no will; operates by constant regularity"},
    {"from": "xz4", "fromPhil": "xunzi", "to": "kz4", "toPhil": "kongzi", "type": "P", "label": "Rectification of names as philosophical and political method"},    {"from": "xz5", "fromPhil": "xunzi", "to": "kz1", "toPhil": "kongzi", "type": "P", "label": "Ritual and law together realize Confucian governance"},
    # === 韩非 ↔ Xunzi, Kongzi, Mengzi, Shen Buhai ===
    {"from": "hf1", "fromPhil": "hanfei", "to": "xz1", "toPhil": "xunzi", "type": "P", "label": "Builds on Xunzi's view of selfish human nature"},
    {"from": "hf1", "fromPhil": "hanfei", "to": "kz2", "toPhil": "kongzi", "type": "N", "label": "Law replaces ritual; virtue is unreliable for governance"},
    {"from": "hf3", "fromPhil": "hanfei", "to": "mz3", "toPhil": "mengzi", "type": "N", "label": "People are to be controlled, not empowered"},
    {"from": "hf4", "fromPhil": "hanfei", "to": "xz1", "toPhil": "xunzi", "type": "P", "label": "Self-interest as political principle develops Xunzi's insight"},
    {"from": "hf5", "fromPhil": "hanfei", "to": "kz1", "toPhil": "kongzi", "type": "N", "label": "Clear rewards and punishments replace benevolent governance"},    # === 公孙龙 ↔ Xunzi ===
    {"from": "gl1", "fromPhil": "gongsunlong", "to": "xz4", "toPhil": "xunzi", "type": "P", "label": "Logical analysis of names extends Confucian rectification"},
    {"from": "gl3", "fromPhil": "gongsunlong", "to": "xz3", "toPhil": "xunzi", "type": "N", "label": "Universals exist independently vs things are concrete"},    # === 董仲舒 ===
    {"from": "ds1", "fromPhil": "dongzhongshu", "to": "kz2", "toPhil": "kongzi", "type": "P", "label": "Institutionalizes ritual as cosmic-social hierarchy"},
    {"from": "ds2", "fromPhil": "dongzhongshu", "to": "lz1", "toPhil": "laozi", "type": "N", "label": "Heaven has moral purpose, not mere spontaneity"},
    {"from": "ds3", "fromPhil": "dongzhongshu", "to": "kz1", "toPhil": "kongzi", "type": "P", "label": "Benevolence aligns with the yang principle of Heaven"},
    {"from": "ds4", "fromPhil": "dongzhongshu", "to": "kz2", "toPhil": "kongzi", "type": "P", "label": "Confucianism as state orthodoxy institutionalizes ritual"},
    {"from": "ds5", "fromPhil": "dongzhongshu", "to": "mz1", "toPhil": "mengzi", "type": "N", "label": "Human nature needs education to actualize its potential for good"},
    {"from": "ds3", "fromPhil": "dongzhongshu", "to": "xz6", "toPhil": "xunzi", "type": "P", "label": "Yang-yang hierarchy structures society cosmologically"},    # === 王充 ===
    {"from": "wc1", "fromPhil": "wangchong", "to": "ds2", "toPhil": "dongzhongshu", "type": "N", "label": "Heaven has no consciousness; cannot respond to humans"},
    {"from": "wc3", "fromPhil": "wangchong", "to": "mo4", "toPhil": "mozi", "type": "P", "label": "Empirical observation is the basis of knowledge"},
    {"from": "wc4", "fromPhil": "wangchong", "to": "xz3", "toPhil": "xunzi", "type": "P", "label": "Heaven's regularity extends Xunzi's naturalistic heaven"},
    {"from": "wc2", "fromPhil": "wangchong", "to": "lz1", "toPhil": "laozi", "type": "P", "label": "Material qi constitutes reality; extends Daoist naturalism"},    # === 韩愈 ===
    {"from": "hy1", "fromPhil": "han_yu", "to": "kz1", "toPhil": "kongzi", "type": "P", "label": "Recovers the original Confucian Way from Daoist and Buddhist influence"},
    {"from": "hy3", "fromPhil": "han_yu", "to": "lz1", "toPhil": "laozi", "type": "N", "label": "Daoism and Buddhism are threats to social order"},
    {"from": "hy2", "fromPhil": "han_yu", "to": "kz10", "toPhil": "kongzi", "type": "P", "label": "Dao tong: the legitimate transmission of the Confucian Way"},    # === 王弼 ===
    {"from": "wb1", "fromPhil": "wangbi", "to": "lz1", "toPhil": "laozi", "type": "P", "label": "Non-being (Wu) as the root of Being develops Laozi"},
    {"from": "wb1", "fromPhil": "wangbi", "to": "lz4", "toPhil": "laozi", "type": "P", "label": "Being comes from non-being; extends reversal of Dao"},
    {"from": "wb2", "fromPhil": "wangbi", "to": "kz4", "toPhil": "kongzi", "type": "N", "label": "Meaning transcends words and names; beyond rectification of names"},    # === 郭象 ===
    {"from": "gx1", "fromPhil": "guoxiang", "to": "wb1", "toPhil": "wangbi", "type": "N", "label": "Self-transformation: things change by themselves, not from non-being"},
    {"from": "gx2", "fromPhil": "guoxiang", "to": "zz1", "toPhil": "zhuangzi", "type": "P", "label": "Each thing is naturally sufficient; develops Zhuangzi's self-so"},    # === 智顗 ===
    {"from": "zy1", "fromPhil": "zhiyi", "to": "xzng1", "toPhil": "xuanzang", "type": "N", "label": "Threefold truth unites emptiness and provisional existence"},
    {"from": "zy2", "fromPhil": "zhiyi", "to": "lz1", "toPhil": "laozi", "type": "P", "label": "One mind contains all — resonates with Daoist unity"},    # === 玄奘 ===
    {"from": "xzng1", "fromPhil": "xuanzang", "to": "xzng1", "toPhil": "xuanzang", "type": "P", "label": "Consciousness-only extends Yogacara into Chinese thought"},
    {"from": "xzng2", "fromPhil": "xuanzang", "to": "lzr1", "toPhil": "liezi", "type": "N", "label": "Storehouse consciousness vs Daoist spontaneity"},
    # === 慧能 ===
    {"from": "hn1", "fromPhil": "huineng", "to": "zy3", "toPhil": "zhiyi", "type": "N", "label": "Sudden enlightenment, not gradual practice"},
    {"from": "hn3", "fromPhil": "huineng", "to": "mz1", "toPhil": "mengzi", "type": "P", "label": "Bodhi is present in everyone — extends Mencius's innate goodness"},
    {"from": "hn5", "fromPhil": "huineng", "to": "cy3", "toPhil": "chengyi", "type": "N", "label": "Direct pointing to the mind, not investigation of things"},    # === 法藏 ===
    {"from": "fz1", "fromPhil": "fazang", "to": "zy2", "toPhil": "zhiyi", "type": "P", "label": "Huayan interpenetration develops Tiantai unity of mind"},
    {"from": "fz3", "fromPhil": "fazang", "to": "zz8", "toPhil": "zhuangzi", "type": "P", "label": "Each thing reflects all others — resonates with Zhuangzi's unity"},    # === 柳宗元 ===
    {"from": "lzy1", "fromPhil": "liuzongyuan", "to": "xz3", "toPhil": "xunzi", "type": "P", "label": "Heaven has no will; extends Xunzi's naturalistic view"},
    {"from": "lzy2", "fromPhil": "liuzongyuan", "to": "kz4", "toPhil": "kongzi", "type": "P", "label": "Institutional reform as modern rectification of names"},    # === 周敦颐 ===
    {"from": "zdy1", "fromPhil": "zhou_dunyi", "to": "lz1", "toPhil": "laozi", "type": "P", "label": "Taiji (Supreme Ultimate) as the source develops Daoist cosmology"},
    {"from": "zdy2", "fromPhil": "zhou_dunyi", "to": "kz3", "toPhil": "kongzi", "type": "P", "label": "The sage embodies the supreme principle as the ideal Junzi"},    # === 张载 ===
    {"from": "zhang1", "fromPhil": "zhangzai", "to": "wc2", "toPhil": "wangchong", "type": "P", "label": "Qi as fundamental substance develops Wang Chong's materialism"},
    {"from": "zhang2", "fromPhil": "zhangzai", "to": "kz1", "toPhil": "kongzi", "type": "P", "label": "All people are my kin extends Ren to universal benevolence"},
    {"from": "zhang1", "fromPhil": "zhangzai", "to": "zx1", "toPhil": "zhuxi", "type": "N", "label": "Qi is primary, not principle"},    # === 程颢 ===
    {"from": "ch1", "fromPhil": "chenghao", "to": "mz2", "toPhil": "mengzi", "type": "P", "label": "Ren as forming one body with all things develops four sprouts"},
    {"from": "ch2", "fromPhil": "chenghao", "to": "kz1", "toPhil": "kongzi", "type": "P", "label": "Unity of Heaven and humanity fulfills Confucian benevolence"},    # === 程颐 ===
    {"from": "cy1", "fromPhil": "chengyi", "to": "lz1", "toPhil": "laozi", "type": "N", "label": "Li (principle) is the true Dao, not formless nothingness"},
    {"from": "cy3", "fromPhil": "chengyi", "to": "kz2", "toPhil": "kongzi", "type": "P", "label": "Investigating things extends the moral meaning of ritual"},
    {"from": "cy4", "fromPhil": "chengyi", "to": "xz1", "toPhil": "xunzi", "type": "P", "label": "Preserve heavenly principle, eliminate desire echoes Xunzi"},    # === 朱熹 ===
    {"from": "zx1", "fromPhil": "zhuxi", "to": "cy1", "toPhil": "chengyi", "type": "P", "label": "Systematizes Li as the metaphysical foundation of all things"},
    {"from": "zx2", "fromPhil": "zhuxi", "to": "cy3", "toPhil": "chengyi", "type": "P", "label": "Investigation of things leads to complete knowledge"},
    {"from": "zx3", "fromPhil": "zhuxi", "to": "xz1", "toPhil": "xunzi", "type": "P", "label": "Desire must be restrained, echoing Xunzi's emphasis on discipline"},
    {"from": "zx4", "fromPhil": "zhuxi", "to": "kz2", "toPhil": "kongzi", "type": "P", "label": "The Great Learning as the path of self-cultivation"},
    {"from": "zx1", "fromPhil": "zhuxi", "to": "zdy1", "toPhil": "zhou_dunyi", "type": "P", "label": "Principle (Li) develops the Supreme Ultimate into metaphysics"},
    {"from": "zx7", "fromPhil": "zhuxi", "to": "ch1", "toPhil": "chenghao", "type": "N", "label": "Investigation of things, not inner experience, is the method"},    # === 陆九渊 ===
    {"from": "ljy1", "fromPhil": "lu_jiuyuan", "to": "zx1", "toPhil": "zhuxi", "type": "N", "label": "The mind IS principle; no need to investigate external things"},
    {"from": "ljy2", "fromPhil": "lu_jiuyuan", "to": "mz1", "toPhil": "mengzi", "type": "P", "label": "The mind's capacity for moral knowing inherits Mencius"},    {"from": "ljy3", "fromPhil": "lu_jiuyuan", "to": "ch1", "toPhil": "chenghao", "type": "P", "label": "Establish the great root extends the unity of Heaven and humanity"},    # === 王阳明 ===
    {"from": "wy1", "fromPhil": "wangyangming", "to": "zx2", "toPhil": "zhuxi", "type": "N", "label": "Knowledge is innate, not acquired through external investigation"},
    {"from": "wy2", "fromPhil": "wangyangming", "to": "kz1", "toPhil": "kongzi", "type": "P", "label": "Unifies knowledge and action as extension of benevolence"},
    {"from": "wy3", "fromPhil": "wangyangming", "to": "mz1", "toPhil": "mengzi", "type": "P", "label": "Restores Mencius's innate goodness as the foundation"},
    {"from": "wy3", "fromPhil": "wangyangming", "to": "zx1", "toPhil": "zhuxi", "type": "N", "label": "Mind IS principle; no separation of li and qi"},
    {"from": "wy6", "fromPhil": "wangyangming", "to": "cy3", "toPhil": "chengyi", "type": "N", "label": "Knowing without acting is not true knowing"},
    {"from": "wy5", "fromPhil": "wangyangming", "to": "ljy1", "toPhil": "lu_jiuyuan", "type": "P", "label": "Develops Lu's mind-is-principle into full philosophical system"},    # === 罗钦顺 ===
    {"from": "lq1", "fromPhil": "luojiushun", "to": "zx1", "toPhil": "zhuxi", "type": "N", "label": "Material force (qi) is primary, not principle (li)"},
    {"from": "lq2", "fromPhil": "luojiushun", "to": "zx1", "toPhil": "zhuxi", "type": "N", "label": "Principle cannot exist apart from material force"},
    {"from": "lq1", "fromPhil": "luojiushun", "to": "zhang1", "toPhil": "zhangzai", "type": "P", "label": "Agrees with Zhang Zai's qi-based ontology"},    # === 李贽 ===
    {"from": "lzz1", "fromPhil": "li_zhi", "to": "zx3", "toPhil": "zhuxi", "type": "N", "label": "The child-like mind rejects Neo-Confucian moral suppression"},
    {"from": "lzz2", "fromPhil": "li_zhi", "to": "xz1", "toPhil": "xunzi", "type": "N", "label": "Self-interest and desire are natural, not evil"},    # === 黄宗羲 ===
    {"from": "hzz1", "fromPhil": "huangzongxi", "to": "hf3", "toPhil": "hanfei", "type": "N", "label": "Power belongs to the people, not the ruler"},
    {"from": "hzz2", "fromPhil": "huangzongxi", "to": "ds1", "toPhil": "dongzhongshu", "type": "N", "label": "The three bonds are instruments of despotism"},
    {"from": "hzz4", "fromPhil": "huangzongxi", "to": "mz3", "toPhil": "mengzi", "type": "P", "label": "Ministers as co-governors develops people-centered governance"},    # === 顾炎武 ===
    {"from": "gyw1", "fromPhil": "guyanwu", "to": "zx4", "toPhil": "zhuxi", "type": "N", "label": "Scholarship must serve the world, not textual exegesis alone"},
    {"from": "gyw2", "fromPhil": "guyanwu", "to": "mo4", "toPhil": "mozi", "type": "P", "label": "Evidential research echoes Mohist empirical rigor"},
    {"from": "gyw3", "fromPhil": "guyanwu", "to": "hzz1", "toPhil": "huangzongxi", "type": "P", "label": "Everyone shares responsibility for society"},    # === 王夫之 ===
    {"from": "wfz1", "fromPhil": "wangfuzhi", "to": "zx1", "toPhil": "zhuxi", "type": "N", "label": "Qi is the fundamental reality, not Li"},
    {"from": "wfz1", "fromPhil": "wangfuzhi", "to": "lq1", "toPhil": "luojiushun", "type": "P", "label": "Agrees that material force is ontologically primary"},
    {"from": "wfz3", "fromPhil": "wangfuzhi", "to": "lz4", "toPhil": "laozi", "type": "P", "label": "The cosmos is in ceaseless transformation, not static return"},
    {"from": "wfz4", "fromPhil": "wangfuzhi", "to": "cy3", "toPhil": "chengyi", "type": "N", "label": "The Way is in concrete affairs, not empty investigation"},    # === 戴震 ===
    {"from": "dz1", "fromPhil": "daizhen", "to": "zx3", "toPhil": "zhuxi", "type": "N", "label": "Eliminating desire is oppressive; principle cannot be used to kill people"},
    {"from": "dz2", "fromPhil": "daizhen", "to": "xz1", "toPhil": "xunzi", "type": "N", "label": "Desire and principle are not opposed; extends Xunzi's naturalism"},    {"from": "dz3", "fromPhil": "daizhen", "to": "gyw2", "toPhil": "guyanwu", "type": "P", "label": "Precise philology as the path to truth extends evidential research"},    # === 谭嗣同 ===
    {"from": "ts1", "fromPhil": "tan_sitong", "to": "kz1", "toPhil": "kongzi", "type": "P", "label": "Ren (benevolence) reinterpreted for modern reform"},
    {"from": "ts2", "fromPhil": "tan_sitong", "to": "ds1", "toPhil": "dongzhongshu", "type": "N", "label": "The three bonds must be destroyed for individual liberty"},
    {"from": "ts3", "fromPhil": "tan_sitong", "to": "zz2", "toPhil": "zhuangzi", "type": "P", "label": "Interconnectedness (Tong) resonates with Zhuangzi's equality of things"},
    # === 康有为 ===
    {"from": "kyw1", "fromPhil": "kangyouwei", "to": "kz1", "toPhil": "kongzi", "type": "P", "label": "Datong (Great Harmony) develops Confucian benevolence into utopia"},
    {"from": "kyw3", "fromPhil": "kangyouwei", "to": "kz2", "toPhil": "kongzi", "type": "N", "label": "Abolish social distinctions that ritual once upheld"},
    {"from": "kyw2", "fromPhil": "kangyouwei", "to": "ds4", "toPhil": "dongzhongshu", "type": "P", "label": "Confucianism as reform ideology institutionalizes change"},    # === 梁启超 ===
    {"from": "lqc1", "fromPhil": "liangqichao", "to": "kyw1", "toPhil": "kangyouwei", "type": "P", "label": "New Citizen develops Datong into national modernization"},
    {"from": "lqc2", "fromPhil": "liangqichao", "to": "kz1", "toPhil": "kongzi", "type": "P", "label": "Preserve Chinese moral core while adopting Western ideas"},
    {"from": "lqc4", "fromPhil": "liangqichao", "to": "kz5", "toPhil": "kongzi", "type": "P", "label": "Freedom as responsibility develops Confucian self-cultivation"},    # === 章太炎 ===
    {"from": "zty1", "fromPhil": "zhangtaiyan", "to": "kz1", "toPhil": "kongzi", "type": "P", "label": "National essence preserves Confucian identity through revolution"},
    {"from": "zty3", "fromPhil": "zhangtaiyan", "to": "xzng1", "toPhil": "xuanzang", "type": "P", "label": "Yogacara combined with Confucian self-cultivation"},    # === 熊十力 ===
    {"from": "xsl1", "fromPhil": "xiongshili", "to": "wy3", "toPhil": "wangyangming", "type": "P", "label": "Mind-body as substance develops Wang's mind-is-principle"},
    {"from": "xsl2", "fromPhil": "xiongshili", "to": "wfz1", "toPhil": "wangfuzhi", "type": "P", "label": "Unity of substance and function resolves qi vs li debate"},
    {"from": "xsl3", "fromPhil": "xiongshili", "to": "kz1", "toPhil": "kongzi", "type": "P", "label": "Original Confucianism is metaphysical, not merely ethical"},    # === 梁漱溟 ===
    {"from": "lsm1", "fromPhil": "liangshuming", "to": "kz1", "toPhil": "kongzi", "type": "P", "label": "Chinese culture oriented toward harmony and Ren"},
    {"from": "lsm2", "fromPhil": "liangshuming", "to": "kz6", "toPhil": "kongzi", "type": "P", "label": "Intuition over intellect extends the Doctrine of the Mean"},
    {"from": "lsm3", "fromPhil": "liangshuming", "to": "wfz3", "toPhil": "wangfuzhi", "type": "P", "label": "Rural reconstruction continues Confucian social ideal"},    # === 冯友兰 ===
    {"from": "fyl2", "fromPhil": "fengyoulan", "to": "wy2", "toPhil": "wangyangming", "type": "P", "label": "Synthesizes Neo-Confucianism into four realms of understanding"},
    {"from": "fyl1", "fromPhil": "fengyoulan", "to": "zz2", "toPhil": "zhuangzi", "type": "P", "label": "Negative method draws from Zhuangzi's ineffability"},
    {"from": "fyl3", "fromPhil": "fengyoulan", "to": "zx1", "toPhil": "zhuxi", "type": "P", "label": "Reconstructs Zhu Xi's Li as modern metaphysical system"},
    {"from": "fyl4", "fromPhil": "fengyoulan", "to": "xsl3", "toPhil": "xiongshili", "type": "P", "label": "Confucian philosophy as rational development of Chinese thought"},    # === 牟宗三 ===
    {"from": "mzs1", "fromPhil": "mouzongsan", "to": "wy3", "toPhil": "wangyangming", "type": "P", "label": "Develops Wang's mind-is-principle into moral metaphysics"},
    {"from": "mzs2", "fromPhil": "mouzongsan", "to": "zx2", "toPhil": "zhuxi", "type": "N", "label": "Intellectual intuition, not investigation of things, yields knowledge"},
    {"from": "mzs3", "fromPhil": "mouzongsan", "to": "mz1", "toPhil": "mengzi", "type": "P", "label": "Mencius's moral sprouts ground the mind-body philosophy"},
    {"from": "mzs4", "fromPhil": "mouzongsan", "to": "fyl1", "toPhil": "fengyoulan", "type": "N", "label": "Intellectual intuition transcends Feng's rational methodology"},    # === 唐君毅 ===
    {"from": "tjy1", "fromPhil": "tangjunyi", "to": "mz1", "toPhil": "mengzi", "type": "P", "label": "The moral ideal extends Mencius's innate goodness"},
    {"from": "tjy2", "fromPhil": "tangjunyi", "to": "mzs3", "toPhil": "mouzongsan", "type": "P", "label": "Nine horizons develop the moral mind's metaphysical scope"},
    {"from": "tjy4", "fromPhil": "tangjunyi", "to": "fyl2", "toPhil": "fengyoulan", "type": "P", "label": "Empathy as foundation of knowledge extends four realms"},    # === 钱穆 ===
    {"from": "qm1", "fromPhil": "qianmu", "to": "kz1", "toPhil": "kongzi", "type": "P", "label": "Chinese cultural tradition has its own coherent spiritual system"},
    {"from": "qm3", "fromPhil": "qianmu", "to": "wy2", "toPhil": "wangyangming", "type": "P", "label": "Unity of knowledge and action is China's unique contribution"},
    {"from": "qm4", "fromPhil": "qianmu", "to": "lsm1", "toPhil": "liangshuming", "type": "P", "label": "Traditional culture can address modern global challenges"},
    # === 申不害 ↔ Xunzi, 韩非, 孔子 ===
    {"from": "sbh1", "fromPhil": "shen_buhai", "to": "hf2", "toPhil": "hanfei", "type": "P", "label": "Administrative method (Shu) is the foundation of Legalist governance"},
    {"from": "sbh2", "fromPhil": "shen_buhai", "to": "kz4", "toPhil": "kongzi", "type": "N", "label": "Matching titles to performance replaces moral rectification"},
    {"from": "sbh3", "fromPhil": "shen_buhai", "to": "xz1", "toPhil": "xunzi", "type": "P", "label": "Human nature is self-interested; rulers must manage through technique"},
    # === 邹衍 ↔ 董仲舒, 老子 ===
    {"from": "zyan1", "fromPhil": "zouyan", "to": "ds2", "toPhil": "dongzhongshu", "type": "P", "label": "Yin-Yang Five Elements develops Heaven-human resonance into systematic cosmology"},
    {"from": "zyan2", "fromPhil": "zouyan", "to": "ds3", "toPhil": "dongzhongshu", "type": "P", "label": "Five Virtues cycle explains dynastic change — extends yang-yin hierarchy"},
    {"from": "zyan3", "fromPhil": "zouyan", "to": "lz1", "toPhil": "laozi", "type": "N", "label": "Systematic cosmology replaces the ineffability of the Dao"},
    # === 魏源 ↔ 顾炎武 ===
    {"from": "wyu1", "fromPhil": "weiyuan", "to": "gyw2", "toPhil": "guyanwu", "type": "P", "label": "Practical geography extends evidential research into world knowledge"},
    {"from": "wyu3", "fromPhil": "weiyuan", "to": "hzz1", "toPhil": "huangzongxi", "type": "P", "label": "Reform through knowledge continues Confucian social ideal"},
    {"from": "wyu2", "fromPhil": "weiyuan", "to": "lzy1", "toPhil": "liuzongyuan", "type": "P", "label": "Understanding the actual world is prerequisite for institutional reform"},
    # === 嵇康 ↔ Laozi, Zhuangzi ===
    {"from": "jk1", "fromPhil": "jikang", "to": "lz2", "toPhil": "laozi", "type": "P", "label": "Reject artificial social norms extends Daoist non-action"},
    {"from": "jk2", "fromPhil": "jikang", "to": "zz4", "toPhil": "zhuangzi", "type": "P", "label": "Music as natural harmony develops Zhuangzi's aesthetics"},
    {"from": "jk3", "fromPhil": "jikang", "to": "xz1", "toPhil": "xunzi", "type": "N", "label": "Natural spontaneity opposes Xunzi's emphasis on artificial transformation"},
    # === 杨雄 ↔ 孟子, 老子 ===
    {"from": "yx3", "fromPhil": "yangxiong", "to": "mz1", "toPhil": "mengzi", "type": "N", "label": "Human nature is mixed good and evil, not purely good"},
    {"from": "yx2", "fromPhil": "yangxiong", "to": "lz1", "toPhil": "laozi", "type": "P", "label": "The Great Mystery develops Daoist cosmological thinking"},
    {"from": "yx1", "fromPhil": "yangxiong", "to": "kz6", "toPhil": "kongzi", "type": "P", "label": "Model Sayings continues the Confucian tradition in aphoristic form"},
    # === 龚自珍 ↔ 戴震 ===
    {"from": "gzz1", "fromPhil": "gongzizhen", "to": "dz1", "toPhil": "daizhen", "type": "P", "label": "Institutional reform extends Dai Zhen's critique of oppressive principle"},
    {"from": "gzz2", "fromPhil": "gongzizhen", "to": "wfz3", "toPhil": "wangfuzhi", "type": "P", "label": "All things are in flux continues Wang Fuzhi's dynamic cosmos"},
    {"from": "gzz3", "fromPhil": "gongzizhen", "to": "hzz2", "toPhil": "huangzongxi", "type": "P", "label": "Decentralization of power continues critique of autocracy"},
    # === 劳思光 ↔ 牟宗三, 冯友兰 ===
    {"from": "lsg1", "fromPhil": "laosiguang", "to": "mzs1", "toPhil": "mouzongsan", "type": "P", "label": "Critical reconstruction complements Mou's moral metaphysics"},
    {"from": "lsg2", "fromPhil": "laosiguang", "to": "wy3", "toPhil": "wangyangming", "type": "P", "label": "Confucian moral philosophy centered on heart-mind extends Wang Yangming"},
    {"from": "lsg4", "fromPhil": "laosiguang", "to": "fyl3", "toPhil": "fengyoulan", "type": "N", "label": "Neo-Confucianism unifies metaphysics, ethics, epistemology — not just rational system"},
    {"from": "lsg3", "fromPhil": "laosiguang", "to": "qm1", "toPhil": "qianmu", "type": "P", "label": "Critical history of Chinese philosophy extends Qian Mu's cultural analysis"},
]

print(f"Total connections: {len(connections)}")
with open('c:/Users/leoni/Documents/GitHub/philograph/data/chinese-connections.json', 'w', encoding='utf-8') as f:
    json.dump(connections, f, ensure_ascii=False, indent=2)
print("Written to chinese-connections.json")

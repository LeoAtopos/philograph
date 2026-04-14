// app.js
App({
  onLaunch() {
    // 读取本地存储的语言设置
    const lang = wx.getStorageSync('philograph-lang');
    if (lang === 'zh' || lang === 'en') {
      this.globalData.lang = lang;
    } else {
      // 微信系统语言检测
      const sysInfo = wx.getSystemInfoSync();
      this.globalData.lang = (sysInfo.language || '').startsWith('zh') ? 'zh' : 'en';
    }

    // 深色模式跟随系统
    const theme = wx.getSystemInfoSync().theme;
    this.globalData.darkMode = theme !== 'light';
  },

  globalData: {
    lang: 'zh',
    darkMode: true,
    westernPhilosophers: null,
    westernConnections: null,
    chinesePhilosophers: null,
    chineseConnections: null,
  }
});

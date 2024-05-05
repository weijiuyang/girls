

console.log('Service Worker 注册成功');
const worker = new Worker('work.js');
worker.addEventListener('message', e=> {
  console.e.data;
})
// 注册 service worker，service worker 脚本文件为 sw.js
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('./sw.js').then(function () {
      console.log('Service Worker 注册成功');
  });
}

// 监听install事件
self.addEventListener('install', function (e) {
  console.log('Service Worker 状态： install');
});

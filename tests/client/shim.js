// stupid enzyme voodoo bullshit
global.requestAnimationFrame = (callback) => {
  setTimeout(callback, 0);
};

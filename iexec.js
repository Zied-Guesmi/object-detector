module.exports = {
  name: 'object-detection',
  app: {
    type: 'DOCKER',
    envvars: 'XWDOCKERIMAGE=ziedguesmi/object-detection',
  },
  work: {
    cmdline: '',
    dirinuri: 'https://github.com/Zied-Guesmi/object-detection/blob/master/DATADIR.zip?raw=true',
  }
};

module.exports = {
  name: 'object-detector',
  app: {
    type: 'DOCKER',
    envvars: 'XWDOCKERIMAGE=ziedguesmi/object-detector',
  },
  work: {
    cmdline: '',
    dirinuri: 'https://github.com/Zied-Guesmi/object-detector/blob/master/DATADIR.zip?raw=true',
  }
};

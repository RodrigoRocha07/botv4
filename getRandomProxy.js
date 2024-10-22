const fs = require('fs');
const path = require('path');

// Caminhos dos arquivos
const proxyFilePath = path.join(__dirname, 'proxy.txt');
const usedProxyFilePath = path.join(__dirname, 'proxy_usados.txt');
// Salva o arquivo JSON na pasta da extensão do Chrome
const proxyOutputFilePath = path.join(__dirname, 'chrome_proxy_extension', 'current_proxy.json');

// Função para ler proxies do arquivo
function readProxies() {
    const proxies = fs.readFileSync(proxyFilePath, 'utf-8').split('\n').filter(Boolean);
    return proxies;
}

// Função para escrever proxies usados no arquivo
function writeUsedProxy(proxy) {
    fs.appendFileSync(usedProxyFilePath, proxy + '\n');
}

// Função para remover proxy usado do arquivo original
function removeUsedProxy(proxy) {
    let proxies = readProxies();
    proxies = proxies.filter(p => p !== proxy);
    fs.writeFileSync(proxyFilePath, proxies.join('\n') + '\n');
}

// Função para obter um proxy aleatório e atualizar os arquivos
function getRandomProxy() {
    const proxies = readProxies();
    if (proxies.length === 0) {
        console.log('/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_');
        console.log('                  Não existem mais proxys disponiveis.');
        console.log('/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_');
        return null;
    }

    const randomIndex = Math.floor(Math.random() * proxies.length);
    const proxy = proxies[randomIndex];

    writeUsedProxy(proxy);
    removeUsedProxy(proxy);

    console.log('Selected Proxy:', proxy);

    const parts = proxy.split(":");
    const randomProxy = {
        host: parts[0],
        port: parseInt(parts[1]),
        username: parts[2],
        password: parts[3]
    };
    if (proxies.length !== 0){
        console.log('proxy localizada')
        fs.writeFileSync(proxyOutputFilePath, JSON.stringify(randomProxy, null, 2));
        return randomProxy;
    }
}

// Testar a função getRandomProxy
const randomProxy = getRandomProxy();
if (randomProxy) {
    console.log('Random Proxy Details:', randomProxy);
} else {
    console.log('No proxy available.');
}

module.exports = getRandomProxy;
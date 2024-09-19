function readProxyConfig(callback) {
    fetch('current_proxy.json')
        .then(response => response.json())
        .then(data => callback(data))
        .catch(error => console.error('Error reading proxy config:', error));
}

readProxyConfig(function(randomProxy) {
    if (randomProxy) {
        var config = {
            mode: "fixed_servers",
            rules: {
                singleProxy: {
                    scheme: "http",
                    host: randomProxy.host,
                    port: randomProxy.port
                },
                bypassList: ["localhost"]
            }
        };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: randomProxy.username,
                    password: randomProxy.password
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
        );
    } else {
        console.error('No proxy available.');
    }
});

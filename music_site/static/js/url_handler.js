function getFullUrl() {
    return window.location.href;
}

function getUrlParts() {
    return getFullUrl().split('?', 2);
}

function getUrlPath() {
    return getUrlParts()[0];
}

function getUrlDomain() {
    return getUrlPath().split('/', 4).slice(0, 3).join('/');
}

function getUrlGetAttributes() {
    try {
        return getUrlParts()[1].split('&');
    } catch {
        return {length: 0};
    }
}

function getUrlAsDict() {
    let result = {};
    let input_get = getUrlGetAttributes();

    for (let i = 0; i < input_get.length; ++i) {
        let input_get_kv = input_get[i].split('=');
        result[ input_get_kv[0] ] = input_get_kv[1];
    }

    return result;
}
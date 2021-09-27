const API_ROOT = 'http://127.0.0.1:8000/api/';
const API_URL = (url, urlParams) => {
    let params = '';
    if (urlParams) {
        params = Object.entries(urlParams).map(([key, value]) => `${key}=${value}`).join('&');
    }
    return `${API_ROOT}${url}${params ? `?${params}` : ''}`
}


export const get = async (url, headers, urlParams) => {
    let init = {method: "GET"};
    if (headers) {
        init = Object.assign(init, {headers: headers});
    }
    try {
        const response = await fetch(API_URL(url, urlParams), init);
        return await response.json();
    } catch (e) {
        return console.log(e);
    }
}


export const post = async (url, data, headers) => {
    let init = {
        method: "POST",
        headers: {"Content-Type": "application/json"}
    };
    if (headers) {
        init.headers = Object.assign(init.headers, headers);
    }
    if (data) {
        init = Object.assign(init, {body: JSON.stringify(data)});
    }
    try {
        const response = await fetch(API_URL(url), init);
        return await response.json();
    } catch (e) {
        return console.log(e);
    }
}

export const del = async (url, headers) => {
    let init = {method: "DELETE"};
    if (headers) {
        init = Object.assign(init, {headers: headers});
    }
    try {
        const response = await fetch(API_URL(url), init);
        return response;
    } catch (e) {
        return console.log(e);
    }
}

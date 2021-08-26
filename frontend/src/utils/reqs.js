const API_ROOT = 'http://127.0.0.1:8000/api/';
const API_URL = url => `${API_ROOT}${url}`;


export const get = async url => {
    try {
        const data = await fetch(API_URL(url));
        return await data.json();
    } catch (e) {
        return console.log(e);
    }
}

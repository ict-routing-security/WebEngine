import axios from 'axios'
function getUrl(str) {
    let url = 'http://127.0.0.1:8000/api/' + str;
    return url;
}
export default {
    Get: (config) => {
        axios({
            methods: "get",
            url: getUrl(config.url),
            params: config.params
        }).then((res) => {
            stateDetection(res);
            config.callback && config.callback(res);
        })

    },
    Post: () => {
        axios({
            methods: "post",
            url: getUrl(config.url)
        }).then((res) => {
            stateDetection(res);
            config.callback && config.callback(res);
        })
    }

}
//状态检测
let stateDetection = (data, callback) => {
    let status = data.status_code;
    switch (status) {
        case 102:
            break;
        case 103:
            alert(data.content);
            break;
        case 404:
            window.location.href = data.url;
            break;
    }
}
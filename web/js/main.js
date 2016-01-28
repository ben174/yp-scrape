var scrape = {
    init: function () {
    },
    query: function () {
        var ws = new WebSocket("ws://127.0.0.1:8888/scrape/cupcake/94536");
        ws.onmessage = function (data) {
            console.log(data);
        }
    }
};
$(scrape.init);

function create_widget_feed_item(w_json){
    return {"factory_id" : w_json["factory_id"], "line_id" : w_json["line_id"], 
            "widget_id" : w_json["serial_number"], "distance" : w_json["classification"]["std_dist"]};
}

function add_feed_widget(vm, widget){
    vm.feed_widgets.unshift(widget)
}

function feed_vm(){
    var self = this;
    self.feed_widgets = ko.observableArray([]);
}

feedvm = new feed_vm();
ko.applyBindings(feedvm, document.getElementById("sidebar"));

var baseUrl = getUrl .protocol + "//" + getUrl.host;

var socket = io();
socket.on('live_badwidget', function(message) {
    if(typeof(message) == "string"){
        add_feed_widget(feedvm, create_widget_feed_item(JSON.parse(message)));
    } else {
        add_feed_widget(feedvm, create_widget_feed_item(message));
    }
});
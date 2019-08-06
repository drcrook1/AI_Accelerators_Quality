function create_widget_feed_item(f_id, l_id, w_id, d){
    return {"factory_id" : f_id, "line_id" : l_id, "widget_id" : w_id, "distance" : d};
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

add_feed_widget(feedvm, create_widget_feed_item("kitty hawk", "1", "W3", "1"))
add_feed_widget(feedvm, create_widget_feed_item("kitty hawk", "1", "W3", "1"))
add_feed_widget(feedvm, create_widget_feed_item("kitty hawk", "1", "W3", "1"))

var socket = io();
socket.on('live_badwidget', function(message) {
    add_feed_widget(feedvm, message)
});
var getUrl = window.location;
var baseUrl = getUrl .protocol + "//" + getUrl.host;

function get_widget_overview_data(vm){
    var url = baseUrl + counts_widgets_endpoint;
    $.getJSON(url, function(data){
        vm.good_count("Total Good Widgets: " + data["good_count"].toString());
        vm.bad_count("Total Bad Widgets: " + data["bad_count"].toString());
        vm.total_count("Total Widgets: " + data["all_count"].toString());
    });
}

function widget_overview_vm(){
    var self = this;
    self.good_count = ko.observable("Loading good count...");
    self.bad_count = ko.observable("Loading bad count...");
    self.total_count = ko.observable("Loading total count...");
}

widget_overview_vm = new widget_overview_vm();
ko.applyBindings(widget_overview_vm, document.getElementById("overview"));
get_widget_overview_data(widget_overview_vm)